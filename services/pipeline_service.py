from datetime import datetime
import pandas as pd

class PipelineService:
    def __init__(self, st):
        self.st = st

    def add_concern(self, concern):
        """Add a new concern"""
        if concern:
            new_concern = pd.DataFrame({
                'concern': [concern],
                'date_added': [datetime.now()]
            })
            self.st.session_state.concerns_df = pd.concat(
                [self.st.session_state.concerns_df, new_concern], 
                ignore_index=True
            )
            return True
        return False

    def add_question(self, question, related_concern):
        """Add a new question"""
        if question and related_concern:
            new_question = pd.DataFrame({
                'question': [question],
                'related_concern': [related_concern],
                'date_added': [datetime.now()]
            })
            self.st.session_state.questions_df = pd.concat(
                [self.st.session_state.questions_df, new_question], 
                ignore_index=True
            )
            return True
        return False

    def add_decision(self, decision, rationale, related_question):
        """Add a new decision"""
        if decision and rationale and related_question:
            new_decision = pd.DataFrame({
                'decision': [decision],
                'rationale': [rationale],
                'related_question': [related_question],
                'date_added': [datetime.now()]
            })
            self.st.session_state.decisions_df = pd.concat(
                [self.st.session_state.decisions_df, new_decision], 
                ignore_index=True
            )
            return True
        return False

    def add_goal(self, goal, related_decision):
        """Add a new goal"""
        if goal and related_decision:
            new_goal = pd.DataFrame({
                'goal': [goal],
                'related_decision': [related_decision],
                'date_added': [datetime.now()]
            })
            self.st.session_state.goals_df = pd.concat(
                [self.st.session_state.goals_df, new_goal], 
                ignore_index=True
            )
            return True
        return False

    def add_task(self, task, assignee, related_goal):
        """Add a new task"""
        if task and assignee and related_goal:
            new_task = pd.DataFrame({
                'task': [task],
                'assignee': [assignee],
                'related_goal': [related_goal],
                'status': ['Not Started'],
                'date_added': [datetime.now()]
            })
            self.st.session_state.tasks_df = pd.concat(
                [self.st.session_state.tasks_df, new_task], 
                ignore_index=True
            )
            return True
        return False

    def get_decision_data(self, decision):
        """Get all related data for a decision"""
        decision_row = self.st.session_state.decisions_df[
            self.st.session_state.decisions_df['decision'] == decision
        ].iloc[0]
        
        question = decision_row['related_question']
        question_row = self.st.session_state.questions_df[
            self.st.session_state.questions_df['question'] == question
        ].iloc[0]
        
        return {
            'decision': decision,
            'rationale': decision_row['rationale'],
            'question': question,
            'concern': question_row['related_concern']
        }

    def get_goals_for_decision(self, decision):
        """Get all goals related to a decision"""
        return self.st.session_state.goals_df[
            self.st.session_state.goals_df['related_decision'] == decision
        ].to_dict('records')

    def get_tasks_for_goal(self, goal):
        """Get all tasks related to a goal"""
        return self.st.session_state.tasks_df[
            self.st.session_state.tasks_df['related_goal'] == goal
        ].to_dict('records')

    def update_concern(self, old_concern, new_concern):
        """Update a concern and cascade the change to related items"""
        if old_concern and new_concern:
            # Update the concern itself
            mask = self.st.session_state.concerns_df['concern'] == old_concern
            self.st.session_state.concerns_df.loc[mask, 'concern'] = new_concern
            
            # Update related questions
            mask = self.st.session_state.questions_df['related_concern'] == old_concern
            self.st.session_state.questions_df.loc[mask, 'related_concern'] = new_concern
            return True
        return False

    def update_question(self, old_question, new_question, new_related_concern=None):
        """Update a question and cascade the change to related items"""
        if old_question and new_question:
            # Update the question itself
            mask = self.st.session_state.questions_df['question'] == old_question
            self.st.session_state.questions_df.loc[mask, 'question'] = new_question
            if new_related_concern:
                self.st.session_state.questions_df.loc[mask, 'related_concern'] = new_related_concern
            
            # Update related decisions
            mask = self.st.session_state.decisions_df['related_question'] == old_question
            self.st.session_state.decisions_df.loc[mask, 'related_question'] = new_question
            return True
        return False

    def update_decision(self, old_decision, new_decision, new_rationale=None, new_related_question=None):
        """Update a decision and cascade the change to related items"""
        if old_decision and new_decision:
            # Update the decision itself
            mask = self.st.session_state.decisions_df['decision'] == old_decision
            self.st.session_state.decisions_df.loc[mask, 'decision'] = new_decision
            if new_rationale:
                self.st.session_state.decisions_df.loc[mask, 'rationale'] = new_rationale
            if new_related_question:
                self.st.session_state.decisions_df.loc[mask, 'related_question'] = new_related_question
            
            # Update related goals
            mask = self.st.session_state.goals_df['related_decision'] == old_decision
            self.st.session_state.goals_df.loc[mask, 'related_decision'] = new_decision
            return True
        return False

    def update_goal(self, old_goal, new_goal, new_related_decision=None):
        """Update a goal and cascade the change to related items"""
        if old_goal and new_goal:
            # Update the goal itself
            mask = self.st.session_state.goals_df['goal'] == old_goal
            self.st.session_state.goals_df.loc[mask, 'goal'] = new_goal
            if new_related_decision:
                self.st.session_state.goals_df.loc[mask, 'related_decision'] = new_related_decision
            
            # Update related tasks
            mask = self.st.session_state.tasks_df['related_goal'] == old_goal
            self.st.session_state.tasks_df.loc[mask, 'related_goal'] = new_goal
            return True
        return False

    def update_task(self, old_task, new_task_data):
        """Update a task"""
        if old_task and new_task_data:
            mask = self.st.session_state.tasks_df['task'] == old_task
            for key, value in new_task_data.items():
                if value:
                    self.st.session_state.tasks_df.loc[mask, key] = value
            return True
        return False

    def delete_concern(self, concern):
        """Delete a concern and all related items"""
        if concern:
            # Get related questions
            related_questions = self.st.session_state.questions_df[
                self.st.session_state.questions_df['related_concern'] == concern
            ]['question'].tolist()
            
            # Delete related questions and their children
            for question in related_questions:
                self.delete_question(question)
            
            # Delete the concern
            self.st.session_state.concerns_df = self.st.session_state.concerns_df[
                self.st.session_state.concerns_df['concern'] != concern
            ]
            return True
        return False

    def delete_question(self, question):
        """Delete a question and all related items"""
        if question:
            # Get related decisions
            related_decisions = self.st.session_state.decisions_df[
                self.st.session_state.decisions_df['related_question'] == question
            ]['decision'].tolist()
            
            # Delete related decisions and their children
            for decision in related_decisions:
                self.delete_decision(decision)
            
            # Delete the question
            self.st.session_state.questions_df = self.st.session_state.questions_df[
                self.st.session_state.questions_df['question'] != question
            ]
            return True
        return False

    def delete_decision(self, decision):
        """Delete a decision and all related items"""
        if decision:
            # Get related goals
            related_goals = self.st.session_state.goals_df[
                self.st.session_state.goals_df['related_decision'] == decision
            ]['goal'].tolist()
            
            # Delete related goals and their children
            for goal in related_goals:
                self.delete_goal(goal)
            
            # Delete the decision
            self.st.session_state.decisions_df = self.st.session_state.decisions_df[
                self.st.session_state.decisions_df['decision'] != decision
            ]
            return True
        return False

    def delete_goal(self, goal):
        """Delete a goal and all related items"""
        if goal:
            # Delete related tasks
            self.st.session_state.tasks_df = self.st.session_state.tasks_df[
                self.st.session_state.tasks_df['related_goal'] != goal
            ]
            
            # Delete the goal
            self.st.session_state.goals_df = self.st.session_state.goals_df[
                self.st.session_state.goals_df['goal'] != goal
            ]
            return True
        return False

    def delete_task(self, task):
        """Delete a task"""
        if task:
            self.st.session_state.tasks_df = self.st.session_state.tasks_df[
                self.st.session_state.tasks_df['task'] != task
            ]
            return True
        return False