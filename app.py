import streamlit as st
import pandas as pd
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import io

class DecisionPipeline:
    def __init__(self):
        # Initialize session state if not exists
        if 'concerns_df' not in st.session_state:
            st.session_state.concerns_df = pd.DataFrame(columns=['concern', 'date_added'])
        if 'questions_df' not in st.session_state:
            st.session_state.questions_df = pd.DataFrame(columns=['question', 'related_concern', 'date_added'])
        if 'decisions_df' not in st.session_state:
            st.session_state.decisions_df = pd.DataFrame(columns=['decision', 'rationale', 'related_question', 'date_added'])
        if 'goals_df' not in st.session_state:
            st.session_state.goals_df = pd.DataFrame(columns=['goal', 'related_decision', 'date_added'])
        if 'tasks_df' not in st.session_state:
            st.session_state.tasks_df = pd.DataFrame(columns=['task', 'assignee', 'related_goal', 'status', 'date_added'])
        
    def generate_decision_graph(self, decision):
        """Generate NetworkX graph for a specific decision"""
        G = nx.DiGraph()

        # Find the related question
        related_question = st.session_state.decisions_df[
            st.session_state.decisions_df['decision'] == decision
        ]['related_question'].iloc[0]

        # Find the related concern
        related_concern = st.session_state.questions_df[
            st.session_state.questions_df['question'] == related_question
        ]['related_concern'].iloc[0]

        # Get the rationale
        rationale = st.session_state.decisions_df[
            st.session_state.decisions_df['decision'] == decision
        ]['rationale'].iloc[0]

        # Add main nodes
        G.add_node('c1', text=f"Concern:\n{related_concern}", node_type='concern')
        G.add_node('q1', text=f"Question:\n{related_question}", node_type='question')
        G.add_node('d1', text=f"Decision:\n{decision}", node_type='decision')
        G.add_node('r1', text=f"Rationale:\n{rationale}", node_type='rationale')

        # Add basic edges
        G.add_edge('c1', 'q1')
        G.add_edge('q1', 'd1')
        G.add_edge('d1', 'r1')

        # Add goals
        related_goals = st.session_state.goals_df[
            st.session_state.goals_df['related_decision'] == decision
        ]

        for idx, goal in related_goals.iterrows():
            g_node_id = f"g{idx}"
            G.add_node(g_node_id, text=f"Goal:\n{goal['goal']}", node_type='goal')
            G.add_edge('d1', g_node_id)

            # Add tasks
            related_tasks = st.session_state.tasks_df[
                st.session_state.tasks_df['related_goal'] == goal['goal']
            ]
            for t_idx, task in related_tasks.iterrows():
                t_node_id = f"t{t_idx}"
                G.add_node(t_node_id, text=f"Task:\n{task['task']}\nAssignee: {task['assignee']}", 
                          node_type='task')
                G.add_edge(g_node_id, t_node_id)

        return G

    def display_graph(self, decision):
        """Display the decision graph using matplotlib"""
        G = self.generate_decision_graph(decision)

        # Create plot
        fig, ax = plt.subplots(figsize=(15, 10))

        # Custom position calculations for triangular layout
        pos = {}
        pos['d1'] = (0.5, 1.0)  # Decision
        pos['r1'] = (0.5, 0.8)  # Rationale
        pos['q1'] = (0.25, 0.6)  # Question
        pos['c1'] = (0, 0.2)  # Concern

        # Calculate positions for goals and tasks
        goals = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'goal']
        tasks = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'task']

        for i, goal in enumerate(goals):
            pos[goal] = (0.75, 0.6)  # Right side

        for i, task in enumerate(tasks):
            pos[task] = (1.0, 0.2)  # Far right

        # Colors for different node types
        colors = {
            'concern': '#ff9999',    # Light red
            'question': '#99ff99',   # Light green
            'decision': '#9999ff',   # Light blue
            'rationale': '#ffcc99',  # Light orange
            'goal': '#ffff99',       # Light yellow
            'task': '#ff99ff'        # Light purple
        }

        # Draw nodes
        for node in G.nodes():
            node_type = G.nodes[node]['node_type']
            nx.draw_networkx_nodes(G, pos, 
                                 nodelist=[node],
                                 node_color=colors[node_type],
                                 node_size=3000,
                                 alpha=0.7)

        # Draw edges
        nx.draw_networkx_edges(G, pos, 
                             edge_color='gray',
                             arrows=True,
                             arrowsize=20,
                             connectionstyle='arc3,rad=0.2')

        # Add labels
        labels = {}
        for node in G.nodes():
            text = G.nodes[node]['text']
            wrapped_text = '\n'.join([text[i:i+20] for i in range(0, len(text), 20)])
            labels[node] = wrapped_text

        nx.draw_networkx_labels(G, pos, labels, font_size=8)

        plt.title(f"Decision Pipeline", fontsize=16, pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Convert plot to image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        return buf

    def save_to_excel(self, filename='decision_pipeline.xlsx'):
        with pd.ExcelWriter(filename) as writer:
            st.session_state.concerns_df.to_excel(writer, sheet_name='Concerns', index=False)
            st.session_state.questions_df.to_excel(writer, sheet_name='Questions', index=False)
            st.session_state.decisions_df.to_excel(writer, sheet_name='Decisions', index=False)
            st.session_state.goals_df.to_excel(writer, sheet_name='Goals', index=False)
            st.session_state.tasks_df.to_excel(writer, sheet_name='Tasks', index=False)
            
    def load_from_excel(self, filename='decision_pipeline.xlsx'):
        st.session_state.concerns_df = pd.read_excel(filename, sheet_name='Concerns')
        st.session_state.questions_df = pd.read_excel(filename, sheet_name='Questions')
        st.session_state.decisions_df = pd.read_excel(filename, sheet_name='Decisions')
        st.session_state.goals_df = pd.read_excel(filename, sheet_name='Goals')
        st.session_state.tasks_df = pd.read_excel(filename, sheet_name='Tasks')

def add_concern():
    if st.session_state.new_concern:
        new_concern = pd.DataFrame({
            'concern': [st.session_state.new_concern],
            'date_added': [datetime.now()]
        })
        st.session_state.concerns_df = pd.concat([st.session_state.concerns_df, new_concern], ignore_index=True)
        st.session_state.new_concern = ""

def add_question():
    if st.session_state.new_question and st.session_state.selected_concern:
        new_question = pd.DataFrame({
            'question': [st.session_state.new_question],
            'related_concern': [st.session_state.selected_concern],
            'date_added': [datetime.now()]
        })
        st.session_state.questions_df = pd.concat([st.session_state.questions_df, new_question], ignore_index=True)
        st.session_state.new_question = ""

def add_decision():
    if (st.session_state.new_decision and st.session_state.new_rationale and 
            st.session_state.selected_question):
        new_decision = pd.DataFrame({
            'decision': [st.session_state.new_decision],
            'rationale': [st.session_state.new_rationale],
            'related_question': [st.session_state.selected_question],
            'date_added': [datetime.now()]
        })
        st.session_state.decisions_df = pd.concat([st.session_state.decisions_df, new_decision], ignore_index=True)
        st.session_state.new_decision = ""
        st.session_state.new_rationale = ""

def add_goal():
    if st.session_state.new_goal and st.session_state.selected_decision:
        new_goal = pd.DataFrame({
            'goal': [st.session_state.new_goal],
            'related_decision': [st.session_state.selected_decision],
            'date_added': [datetime.now()]
        })
        st.session_state.goals_df = pd.concat([st.session_state.goals_df, new_goal], ignore_index=True)
        st.session_state.new_goal = ""

def add_task():
    if (st.session_state.new_task and st.session_state.new_assignee and 
            st.session_state.selected_goal):
        new_task = pd.DataFrame({
            'task': [st.session_state.new_task],
            'assignee': [st.session_state.new_assignee],
            'related_goal': [st.session_state.selected_goal],
            'status': ['Not Started'],
            'date_added': [datetime.now()]
        })
        st.session_state.tasks_df = pd.concat([st.session_state.tasks_df, new_task], ignore_index=True)
        st.session_state.new_task = ""
        st.session_state.new_assignee = ""

def main():
    st.title("Decision Pipeline")
    
    # Initialize the pipeline
    pipeline = DecisionPipeline()
    
    # Sidebar for adding new items
    with st.sidebar:
        st.header("Add New Items")
        
        # Add Concern
        st.subheader("Add Concern")
        st.text_input("New Concern", key="new_concern")
        st.button("Add Concern", on_click=add_concern)
        
        # Add Question
        st.subheader("Add Question")
        st.text_input("New Question", key="new_question")
        concerns = st.session_state.concerns_df['concern'].tolist()
        st.selectbox("Related Concern", concerns if concerns else [''], key="selected_concern")
        st.button("Add Question", on_click=add_question)
        
        # Add Decision
        st.subheader("Add Decision")
        st.text_input("New Decision", key="new_decision")
        st.text_area("Rationale", key="new_rationale")
        questions = st.session_state.questions_df['question'].tolist()
        st.selectbox("Related Question", questions if questions else [''], key="selected_question")
        st.button("Add Decision", on_click=add_decision)
        
        # Add Goal
        st.subheader("Add Goal")
        st.text_input("New Goal", key="new_goal")
        decisions = st.session_state.decisions_df['decision'].tolist()
        st.selectbox("Related Decision", decisions if decisions else [''], key="selected_decision")
        st.button("Add Goal", on_click=add_goal)
        
        # Add Task
        st.subheader("Add Task")
        st.text_input("New Task", key="new_task")
        st.text_input("Assignee", key="new_assignee")
        goals = st.session_state.goals_df['goal'].tolist()
        st.selectbox("Related Goal", goals if goals else [''], key="selected_goal")
        st.button("Add Task", on_click=add_task)
    
    # Main content area
    decisions = st.session_state.decisions_df['decision'].tolist()
    if decisions:
        selected_decision = st.selectbox("Select Decision to View", decisions)
        if selected_decision:
            # Display the graph
            graph_buf = pipeline.display_graph(selected_decision)
            st.image(graph_buf)
            
            # Display related information
            st.subheader("Decision Details")
            decision_info = st.session_state.decisions_df[
                st.session_state.decisions_df['decision'] == selected_decision
            ].iloc[0]
            st.write(f"**Rationale:** {decision_info['rationale']}")
            
            # Display related goals and tasks
            st.subheader("Related Goals and Tasks")
            related_goals = st.session_state.goals_df[
                st.session_state.goals_df['related_decision'] == selected_decision
            ]
            for _, goal in related_goals.iterrows():
                st.write(f"**Goal:** {goal['goal']}")
                related_tasks = st.session_state.tasks_df[
                    st.session_state.tasks_df['related_goal'] == goal['goal']
                ]
                for _, task in related_tasks.iterrows():
                    st.write(f"- Task: {task['task']} (Assignee: {task['assignee']}, Status: {task['status']})")
    else:
        st.info("No decisions added yet. Use the sidebar to add new items to the pipeline.")

if __name__ == "__main__":
    main()
