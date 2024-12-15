import networkx as nx

class GraphService:
    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def generate_decision_graph(self, decision):
        """Generate NetworkX graph for a specific decision"""
        G = nx.DiGraph()
        
        # Get related data
        decision_data = self.pipeline_service.get_decision_data(decision)
        if not decision_data:
            return None

        # Add decision and rationale nodes
        G.add_node('d1', text=f"Decision:\n{decision}", node_type='decision')
        G.add_node('r1', text=f"Rationale:\n{decision_data['rationale']}", node_type='rationale')
        G.add_edge('d1', 'r1')

        # Track unique concerns to avoid duplicates
        unique_concerns = {}  # concern text -> node id mapping

        # Add questions and their concerns
        for idx, q_data in enumerate(decision_data['questions_data']):
            q_node_id = f"q{idx+1}"
            concern_text = q_data['concern']
            
            # Check if we've already created a node for this concern
            if concern_text in unique_concerns:
                c_node_id = unique_concerns[concern_text]
            else:
                c_node_id = f"c{len(unique_concerns) + 1}"
                unique_concerns[concern_text] = c_node_id
                G.add_node(c_node_id, text=f"Concern:\n{concern_text}", node_type='concern')
            
            G.add_node(q_node_id, text=f"Question:\n{q_data['question']}", node_type='question')
            
            # Connect concern to question and question to decision
            G.add_edge(c_node_id, q_node_id)
            G.add_edge(q_node_id, 'd1')

        # Add goals and tasks
        self._add_goals_and_tasks(G, decision)

        return G

    def _add_goals_and_tasks(self, G, decision):
        """Add goals and tasks to the graph"""
        goals = self.pipeline_service.get_goals_for_decision(decision)
        
        for idx, goal in enumerate(goals):
            g_node_id = f"g{idx}"
            G.add_node(g_node_id, text=f"Goal:\n{goal['goal']}", node_type='goal')
            G.add_edge('d1', g_node_id)

            tasks = self.pipeline_service.get_tasks_for_goal(goal['goal'])
            for t_idx, task in enumerate(tasks):
                t_node_id = f"t{t_idx}"
                G.add_node(t_node_id, 
                          text=f"Task:\n{task['task']}\nAssignee: {task['assignee']}", 
                          node_type='task')
                G.add_edge(g_node_id, t_node_id)
