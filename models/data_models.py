import pandas as pd
from datetime import datetime

class DataFrameModel:
    @staticmethod
    def create_concerns_df():
        return pd.DataFrame(columns=['concern', 'urgency', 'date_added'])
    
    @staticmethod
    def create_questions_df():
        return pd.DataFrame(columns=['question', 'related_concern', 'urgency', 'date_added'])
    
    @staticmethod
    def create_decisions_df():
        # Changed related_question to related_questions to indicate it stores a list
        return pd.DataFrame(columns=['decision', 'rationale', 'related_questions', 'urgency', 'date_added'])
    
    @staticmethod
    def create_goals_df():
        return pd.DataFrame(columns=['goal', 'related_decision', 'urgency', 'date_added'])
    
    @staticmethod
    def create_tasks_df():
        return pd.DataFrame(columns=['task', 'assignee', 'related_goal', 'status', 'urgency', 'date_added'])
    
    @staticmethod
    def create_todos_df():
        return pd.DataFrame(columns=['title', 'details', 'categories', 'importance', 'date_added'])

class PipelineItem:
    def __init__(self, data):
        self.data = data
        self.date_added = datetime.now()
