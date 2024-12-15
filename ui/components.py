import streamlit as st

class Sidebar:
    def __init__(self, pipeline_service):
        self.pipeline_service = pipeline_service

    def render(self):
        """Render the complete sidebar with all input sections"""
        with st.sidebar:
            st.header("Add New Items")
            self._render_concern_section()
            self._render_question_section()
            self._render_decision_section()
            self._render_goal_section()
            self._render_task_section()

    def _render_concern_section(self):
        """Render the concern input section"""
        st.subheader("Add Concern")
        with st.form(key="concern_form"):
            concern = st.text_input("New Concern")
            submit = st.form_submit_button("Add Concern")
            if submit and concern:
                if self.pipeline_service.add_concern(concern):
                    st.success("Concern added successfully!")
                    st.rerun()

    def _render_question_section(self):
        """Render the question input section"""
        st.subheader("Add Question")
        with st.form(key="question_form"):
            question = st.text_input("New Question")
            concerns = st.session_state.concerns_df['concern'].tolist()
            selected_concern = st.selectbox(
                "Related Concern",
                concerns if concerns else ['']
            )
            submit = st.form_submit_button("Add Question")
            if submit and question and selected_concern and selected_concern != '':
                if self.pipeline_service.add_question(question, selected_concern):
                    st.success("Question added successfully!")
                    st.rerun()

    def _render_decision_section(self):
        """Render the decision input section"""
        st.subheader("Add Decision")
        with st.form(key="decision_form"):
            decision = st.text_input("New Decision")
            rationale = st.text_area("Rationale")
            questions = st.session_state.questions_df['question'].tolist()
            selected_question = st.selectbox(
                "Related Question",
                questions if questions else ['']
            )
            submit = st.form_submit_button("Add Decision")
            if submit and decision and rationale and selected_question and selected_question != '':
                if self.pipeline_service.add_decision(decision, rationale, selected_question):
                    st.success("Decision added successfully!")
                    st.rerun()

    def _render_goal_section(self):
        """Render the goal input section"""
        st.subheader("Add Goal")
        with st.form(key="goal_form"):
            goal = st.text_input("New Goal")
            decisions = st.session_state.decisions_df['decision'].tolist()
            selected_decision = st.selectbox(
                "Related Decision",
                decisions if decisions else ['']
            )
            submit = st.form_submit_button("Add Goal")
            if submit and goal and selected_decision and selected_decision != '':
                if self.pipeline_service.add_goal(goal, selected_decision):
                    st.success("Goal added successfully!")
                    st.rerun()

    def _render_task_section(self):
        """Render the task input section"""
        st.subheader("Add Task")
        with st.form(key="task_form"):
            task = st.text_input("New Task")
            assignee = st.text_input("Assignee")
            goals = st.session_state.goals_df['goal'].tolist()
            selected_goal = st.selectbox(
                "Related Goal",
                goals if goals else ['']
            )
            submit = st.form_submit_button("Add Task")
            if submit and task and assignee and selected_goal and selected_goal != '':
                if self.pipeline_service.add_task(task, assignee, selected_goal):
                    st.success("Task added successfully!")
                    st.rerun()

    def _render_concern_section(self):
        """Render the concern input section"""
        st.subheader("Add Concern")
        with st.form(key="concern_form"):
            concern = st.text_input("New Concern")
            urgency = st.slider(
                "Urgency",
                min_value=1,
                max_value=100,
                value=50,
                help="Set the urgency level (1-100)"
            )
            submit = st.form_submit_button("Add Concern")
            if submit and concern:
                if self.pipeline_service.add_concern(concern, urgency):
                    st.success("Concern added successfully!")
                    st.rerun()