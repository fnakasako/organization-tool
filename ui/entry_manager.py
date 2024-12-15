import streamlit as st

class EntryManager:
    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def render(self):
        """Render the entry management interface"""
        st.header("Manage Entries")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Concerns", "Questions", "Decisions", "Goals", "Tasks", "Todos"
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
            
        with tab6:
            self._manage_todos()

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
                
                # Check if there are any concerns before creating the selectbox
                if not st.session_state.concerns_df.empty:
                    new_concern = st.selectbox(
                        "Related Concern",
                        st.session_state.concerns_df['concern'].tolist(),
                        index=st.session_state.concerns_df['concern'].tolist().index(question_data['related_concern'])
                    )
                else:
                    st.warning("No concerns available. Please add concerns first.")
                    new_concern = None
                
                if st.button("Update Question", key="update_question") and new_concern:
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
                new_rationale = st.text_area("New Rationale", value=decision_data.get('rationale', ''), key="edit_rationale")
                
                # Check if there are any questions before creating the selectbox
                if not st.session_state.questions_df.empty:
                    questions_list = st.session_state.questions_df['question'].tolist()
                    related_question = decision_data.get('related_question')
                    if related_question in questions_list:
                        question_index = questions_list.index(related_question)
                    else:
                        question_index = 0
                    
                    new_question = st.selectbox(
                        "Related Question",
                        questions_list,
                        index=question_index
                    )
                else:
                    st.warning("No questions available. Please add questions first.")
                    new_question = None
                
                if st.button("Update Decision", key="update_decision") and new_question:
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
                
                # Check if there are any decisions before creating the selectbox
                if not st.session_state.decisions_df.empty:
                    decisions_list = st.session_state.decisions_df['decision'].tolist()
                    related_decision = goal_data.get('related_decision')
                    if related_decision in decisions_list:
                        decision_index = decisions_list.index(related_decision)
                    else:
                        decision_index = 0
                        
                    new_decision = st.selectbox(
                        "Related Decision",
                        decisions_list,
                        index=decision_index
                    )
                else:
                    st.warning("No decisions available. Please add decisions first.")
                    new_decision = None
                
                if st.button("Update Goal", key="update_goal") and new_decision:
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
                new_assignee = st.text_input("New Assignee", value=task_data.get('assignee', ''), key="edit_assignee")
                
                # Check if there are any goals before creating the selectbox
                if not st.session_state.goals_df.empty:
                    goals_list = st.session_state.goals_df['goal'].tolist()
                    related_goal = task_data.get('related_goal')
                    if related_goal in goals_list:
                        goal_index = goals_list.index(related_goal)
                    else:
                        goal_index = 0
                        
                    new_goal = st.selectbox(
                        "Related Goal",
                        goals_list,
                        index=goal_index
                    )
                else:
                    st.warning("No goals available. Please add goals first.")
                    new_goal = None
                    
                new_status = st.selectbox(
                    "Status",
                    ["Not Started", "In Progress", "Completed"],
                    index=["Not Started", "In Progress", "Completed"].index(task_data.get('status', 'Not Started'))
                )
                
                if st.button("Update Task", key="update_task") and new_goal:
                    new_task_data = {
                        'task': new_task,
                        'assignee': new_assignee,
                        'related_goal': new_goal,
                        'status': new_status
                    }
                    if self.pipeline_service.update_task(selected_task, new_task_data):
                        st.success(f"Updated task to '{new_task}'")

    def _manage_todos(self):
        """Manage todo items"""
        if 'todos_df' in st.session_state and not st.session_state.todos_df.empty:
            todos = st.session_state.todos_df['title'].tolist()
            selected_todo = st.selectbox("Select Todo to Manage", todos, key="manage_todo")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Todo", key="delete_todo"):
                    if self.pipeline_service.delete_todo(selected_todo):
                        st.success(f"Deleted todo '{selected_todo}'")
                        st.rerun()
            
            with col2:
                todo_data = st.session_state.todos_df[
                    st.session_state.todos_df['title'] == selected_todo
                ].iloc[0]
                
                new_title = st.text_input("Title", value=todo_data['title'], key="edit_todo_title")
                new_details = st.text_area("Details", value=todo_data['details'], key="edit_todo_details")
                new_category = st.selectbox(
                    "Category",
                    ["Codebase", "HR", "Business", "Finance", "Other"],
                    index=["Codebase", "HR", "Business", "Finance", "Other"].index(todo_data['category'])
                )
                new_importance = st.slider(
                    "Importance",
                    min_value=1,
                    max_value=100,
                    value=int(todo_data['importance']),
                    key="edit_todo_importance"
                )
                
                if st.button("Update Todo", key="update_todo"):
                    if self.pipeline_service.update_todo(
                        selected_todo,
                        new_title,
                        new_details,
                        new_category,
                        new_importance
                    ):
                        st.success(f"Updated todo '{new_title}'")
                        st.rerun()
        else:
            st.info("No todos available. Add some todos using the sidebar.")
