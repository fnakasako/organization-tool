import streamlit as st

class EntryManager:
    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def render(self):
        """Render the entry management interface"""
        st.header("Manage Entries")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Concerns", "Questions", "Decisions", "Goals", "Tasks"
        ])

        with tab1:
            self._manage_concerns()
        
        with tab2:
            self._manage_questions()
            
        with tab3:
            self._manage_decisions()
            
        with tab4:
            self._manage_goals()
            
        with tab5:
            self._manage_tasks()

    def _manage_concerns(self):
        concerns = st.session_state.concerns_df['concern'].tolist()
        if concerns:
            selected_concern = st.selectbox("Select Concern to Manage", concerns, key="manage_concern")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Concern", key="delete_concern"):
                    if self.pipeline_service.delete_concern(selected_concern):
                        st.success(f"Deleted concern '{selected_concern}' and all related items")
            
            with col2:
                new_concern = st.text_input("New Concern Text", value=selected_concern, key="edit_concern")
                if st.button("Update Concern", key="update_concern"):
                    if self.pipeline_service.update_concern(selected_concern, new_concern):
                        st.success(f"Updated concern to '{new_concern}'")

    def _manage_questions(self):
        questions = st.session_state.questions_df['question'].tolist()
        if questions:
            selected_question = st.selectbox("Select Question to Manage", questions, key="manage_question")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Question", key="delete_question"):
                    if self.pipeline_service.delete_question(selected_question):
                        st.success(f"Deleted question '{selected_question}' and all related items")
            
            with col2:
                question_data = st.session_state.questions_df[
                    st.session_state.questions_df['question'] == selected_question
                ].iloc[0]
                
                new_question = st.text_input("New Question Text", value=selected_question, key="edit_question")
                new_concern = st.selectbox(
                    "Related Concern",
                    st.session_state.concerns_df['concern'].tolist(),
                    index=st.session_state.concerns_df['concern'].tolist().index(question_data['related_concern'])
                )
                
                if st.button("Update Question", key="update_question"):
                    if self.pipeline_service.update_question(selected_question, new_question, new_concern):
                        st.success(f"Updated question to '{new_question}'")

    def _manage_decisions(self):
        decisions = st.session_state.decisions_df['decision'].tolist()
        if decisions:
            selected_decision = st.selectbox("Select Decision to Manage", decisions, key="manage_decision")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Decision", key="delete_decision"):
                    if self.pipeline_service.delete_decision(selected_decision):
                        st.success(f"Deleted decision '{selected_decision}' and all related items")
            
            with col2:
                decision_data = st.session_state.decisions_df[
                    st.session_state.decisions_df['decision'] == selected_decision
                ].iloc[0]
                
                new_decision = st.text_input("New Decision Text", value=selected_decision, key="edit_decision")
                new_rationale = st.text_area("New Rationale", value=decision_data['rationale'], key="edit_rationale")
                new_question = st.selectbox(
                    "Related Question",
                    st.session_state.questions_df['question'].tolist(),
                    index=st.session_state.questions_df['question'].tolist().index(decision_data['related_question'])
                )
                
                if st.button("Update Decision", key="update_decision"):
                    if self.pipeline_service.update_decision(
                        selected_decision, new_decision, new_rationale, new_question
                    ):
                        st.success(f"Updated decision to '{new_decision}'")

    def _manage_goals(self):
        goals = st.session_state.goals_df['goal'].tolist()
        if goals:
            selected_goal = st.selectbox("Select Goal to Manage", goals, key="manage_goal")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Goal", key="delete_goal"):
                    if self.pipeline_service.delete_goal(selected_goal):
                        st.success(f"Deleted goal '{selected_goal}' and all related items")
            
            with col2:
                goal_data = st.session_state.goals_df[
                    st.session_state.goals_df['goal'] == selected_goal
                ].iloc[0]
                
                new_goal = st.text_input("New Goal Text", value=selected_goal, key="edit_goal")
                new_decision = st.selectbox(
                    "Related Decision",
                    st.session_state.decisions_df['decision'].tolist(),
                    index=st.session_state.decisions_df['decision'].tolist().index(goal_data['related_decision'])
                )
                
                if st.button("Update Goal", key="update_goal"):
                    if self.pipeline_service.update_goal(selected_goal, new_goal, new_decision):
                        st.success(f"Updated goal to '{new_goal}'")

    def _manage_tasks(self):
        tasks = st.session_state.tasks_df['task'].tolist()
        if tasks:
            selected_task = st.selectbox("Select Task to Manage", tasks, key="manage_task")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Task", key="delete_task"):
                    if self.pipeline_service.delete_task(selected_task):
                        st.success(f"Deleted task '{selected_task}'")
            
            with col2:
                task_data = st.session_state.tasks_df[
                    st.session_state.tasks_df['task'] == selected_task
                ].iloc[0]
                
                new_task = st.text_input("New Task Text", value=selected_task, key="edit_task")
                new_assignee = st.text_input("New Assignee", value=task_data['assignee'], key="edit_assignee")
                new_goal = st.selectbox(
                    "Related Goal",
                    st.session_state.goals_df['goal'].tolist(),
                    index=st.session_state.goals_df['goal'].tolist().index(task_data['related_goal'])
                )
                new_status = st.selectbox(
                    "Status",
                    ["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress", "Completed"].index(task_data['status'])
                )
                
                if st.button("Update Task", key="update_task"):
                    new_task_data = {
                        'task': new_task,
                        'assignee': new_assignee,
                        'related_goal': new_goal,
                        'status': new_status
                    }
                    if self.pipeline_service.update_task(selected_task, new_task_data):
                        st.success(f"Updated task to '{new_task}'")