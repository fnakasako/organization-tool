import pandas as pd
from models.data_models import DataFrameModel
import ast

class StorageService:
    def __init__(self):
        self.model = DataFrameModel()
    
    def initialize_dataframes(self, st):
        """Initialize all dataframes in Streamlit session state"""
        if 'concerns_df' not in st.session_state:
            st.session_state.concerns_df = self.model.create_concerns_df()
        if 'questions_df' not in st.session_state:
            st.session_state.questions_df = self.model.create_questions_df()
        if 'decisions_df' not in st.session_state:
            st.session_state.decisions_df = self.model.create_decisions_df()
        if 'goals_df' not in st.session_state:
            st.session_state.goals_df = self.model.create_goals_df()
        if 'tasks_df' not in st.session_state:
            st.session_state.tasks_df = self.model.create_tasks_df()
        if 'todos_df' not in st.session_state:
            st.session_state.todos_df = self.model.create_todos_df()

    def save_to_excel(self, st, filename='decision_pipeline.xlsx'):
        """Save all dataframes to Excel"""
        with pd.ExcelWriter(filename) as writer:
            st.session_state.concerns_df.to_excel(writer, sheet_name='Concerns', index=False)
            st.session_state.questions_df.to_excel(writer, sheet_name='Questions', index=False)
            
            # Handle decisions_df with list column
            decisions_df = st.session_state.decisions_df.copy()
            decisions_df['related_questions'] = decisions_df['related_questions'].apply(str)
            decisions_df.to_excel(writer, sheet_name='Decisions', index=False)
            
            st.session_state.goals_df.to_excel(writer, sheet_name='Goals', index=False)
            st.session_state.tasks_df.to_excel(writer, sheet_name='Tasks', index=False)
            
            if 'todos_df' in st.session_state:
                # Handle todos_df with list column
                todos_df = st.session_state.todos_df.copy()
                todos_df['categories'] = todos_df['categories'].apply(str)
                todos_df.to_excel(writer, sheet_name='Todos', index=False)
    
    def load_from_excel(self, st, filename='decision_pipeline.xlsx'):
        """Load all dataframes from Excel"""
        st.session_state.concerns_df = pd.read_excel(filename, sheet_name='Concerns')
        st.session_state.questions_df = pd.read_excel(filename, sheet_name='Questions')
        
        # Handle decisions_df with list column
        decisions_df = pd.read_excel(filename, sheet_name='Decisions')
        decisions_df['related_questions'] = decisions_df['related_questions'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        st.session_state.decisions_df = decisions_df
        
        st.session_state.goals_df = pd.read_excel(filename, sheet_name='Goals')
        st.session_state.tasks_df = pd.read_excel(filename, sheet_name='Tasks')
        
        try:
            # Handle todos_df with list column
            todos_df = pd.read_excel(filename, sheet_name='Todos')
            todos_df['categories'] = todos_df['categories'].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            st.session_state.todos_df = todos_df
        except ValueError:
            # If Todos sheet doesn't exist in older files, create empty DataFrame
            st.session_state.todos_df = self.model.create_todos_df()
