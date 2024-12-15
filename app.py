import streamlit as st
from services.storage_service import StorageService
from services.pipeline_service import PipelineService
from services.graph_service import GraphService
from utils.visualization import GraphVisualizer, CircleVisualizer, PipelineVisualizer
from ui.components import Sidebar
from ui.entry_manager import EntryManager

def initialize_services():
    """Initialize all services needed for the application"""
    storage_service = StorageService()
    storage_service.initialize_dataframes(st)
    
    pipeline_service = PipelineService(st)
    graph_service = GraphService(pipeline_service)
    graph_visualizer = GraphVisualizer()
    circle_visualizer = CircleVisualizer()  # Add CircleVisualizer initialization
    
    return pipeline_service, graph_service, graph_visualizer, circle_visualizer

def render_main_content(pipeline_service, graph_service, graph_visualizer, circle_visualizer):
    """Render the main content area of the application"""
    st.title("Decision Pipeline")
    
    # Add tabs for all visualizations and management
    viz_tab, circles_tab, manage_tab = st.tabs([
        "Pipeline Visualization", 
        "Item Overview", 
        "Manage Entries"
    ])
    
    # Pipeline Visualization Tab
    with viz_tab:
        pipeline_viz = PipelineVisualizer(pipeline_service, graph_service, graph_visualizer)
        pipeline_viz.render()

    # Circles Visualization Tab
    with circles_tab:
        # Create columns for different item types
        col1, col2, col3 = st.columns(3)
        col4, col5 = st.columns(2)

        with col1:
            st.subheader("Concerns")
            concerns_data = [
                {'concern': row['concern'], 'urgency': row['urgency']}
                for _, row in st.session_state.concerns_df.iterrows()
            ]
            if concerns_data:
                svg_content = circle_visualizer.create_circle_graph(concerns_data, 'concern')
                if svg_content:
                    st.components.v1.html(svg_content, height=300)
            else:
                st.info("No concerns added yet")

        with col2:
            st.subheader("Questions")
            questions_data = [
                {'question': row['question'], 'urgency': row['urgency']}
                for _, row in st.session_state.questions_df.iterrows()
            ]
            if questions_data:
                svg_content = circle_visualizer.create_circle_graph(questions_data, 'question')
                if svg_content:
                    st.components.v1.html(svg_content, height=300)
            else:
                st.info("No questions added yet")

        with col3:
            st.subheader("Decisions")
            decisions_data = [
                {'decision': row['decision'], 'urgency': row['urgency']}
                for _, row in st.session_state.decisions_df.iterrows()
            ]
            if decisions_data:
                svg_content = circle_visualizer.create_circle_graph(decisions_data, 'decision')
                if svg_content:
                    st.components.v1.html(svg_content, height=300)
            else:
                st.info("No decisions added yet")

        with col4:
            st.subheader("Goals")
            goals_data = [
                {'goal': row['goal'], 'urgency': row['urgency']}
                for _, row in st.session_state.goals_df.iterrows()
            ]
            if goals_data:
                svg_content = circle_visualizer.create_circle_graph(goals_data, 'goal')
                if svg_content:
                    st.components.v1.html(svg_content, height=300)
            else:
                st.info("No goals added yet")

        with col5:
            st.subheader("Tasks")
            tasks_data = [
                {'task': row['task'], 'urgency': row['urgency']}
                for _, row in st.session_state.tasks_df.iterrows()
            ]
            if tasks_data:
                svg_content = circle_visualizer.create_circle_graph(tasks_data, 'task')
                if svg_content:
                    st.components.v1.html(svg_content, height=300)
            else:
                st.info("No tasks added yet")

    # Management Tab
    with manage_tab:
        entry_manager = EntryManager(pipeline_service)
        entry_manager.render()

def add_file_management(storage_service):
    """Add file upload and download functionality"""
    st.sidebar.header("File Management")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Pipeline Data",
        type="xlsx",
        help="Upload an existing decision pipeline Excel file"
    )
    if uploaded_file is not None:
        try:
            storage_service.load_from_excel(st, uploaded_file)
            st.sidebar.success("Pipeline data loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {str(e)}")
    
    # File download
    if st.sidebar.button("Download Pipeline Data"):
        try:
            storage_service.save_to_excel(st)
            st.sidebar.success("Pipeline data saved to 'decision_pipeline.xlsx'!")
        except Exception as e:
            st.sidebar.error(f"Error saving file: {str(e)}")

def main():
    # Set page config
    st.set_page_config(
        page_title="Decision Pipeline",
        page_icon="🔄",
        layout="wide"
    )
    
    # Initialize all services
    pipeline_service, graph_service, graph_visualizer, circle_visualizer = initialize_services()
    storage_service = StorageService()
    
    # Render sidebar with entry addition and file management
    sidebar = Sidebar(pipeline_service)
    sidebar.render()
    add_file_management(storage_service)
    
    # Render main content
    render_main_content(pipeline_service, graph_service, graph_visualizer, circle_visualizer)

if __name__ == "__main__":
    main()