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
    circle_visualizer = CircleVisualizer()
    
    return pipeline_service, graph_service, graph_visualizer, circle_visualizer

def render_main_content(pipeline_service, graph_service, graph_visualizer, circle_visualizer):
    """Render the main content area of the application"""
    st.title("Decision Pipeline")
    
    # Add tabs for all visualizations and management
    viz_tab, circles_tab, todos_tab, manage_tab = st.tabs([
        "Pipeline Visualization", 
        "Item Overview",
        "To do List",
        "Manage Entries"
    ])
    
    # Pipeline Visualization Tab
    with viz_tab:
        # Add decision selector
        if 'decisions_df' in st.session_state and not st.session_state.decisions_df.empty:
            decisions = st.session_state.decisions_df['decision'].tolist()
            selected_decision = st.selectbox(
                "Select a decision to visualize",
                options=decisions
            )
            pipeline_viz = PipelineVisualizer(pipeline_service, graph_service)
            pipeline_viz.render(selected_decision)
        else:
            st.info("Add some decisions to visualize the pipeline.")
    
    # Circles Visualization Tab
    with circles_tab:
        # Create buttons for different item types
        item_types = {
            "Concerns": ("concerns_df", "concern"),
            "Questions": ("questions_df", "question"),
            "Decisions": ("decisions_df", "decision"),
            "Goals": ("goals_df", "goal"),
            "Tasks": ("tasks_df", "task")
        }
        
        # Create columns for buttons
        cols = st.columns(len(item_types))
        
        # Add buttons for each item type
        for col, (label, (df_name, item_key)) in zip(cols, item_types.items()):
            with col:
                if st.button(label):
                    st.session_state.selected_view = (df_name, item_key)
                
        # Display selected visualization
        if hasattr(st.session_state, 'selected_view') and st.session_state.selected_view is not None:
            df_name, item_key = st.session_state.selected_view
            
            if df_name in st.session_state and not st.session_state[df_name].empty:
                items_data = [
                    {item_key: row[item_key], 'urgency': row['urgency']}
                    for _, row in st.session_state[df_name].iterrows()
                ]
                if items_data:
                    svg_content = circle_visualizer.create_circle_graph(items_data, item_key)
                    if svg_content:
                        st.components.v1.html(svg_content, height=600)
            else:
                st.info(f"No {item_key}s added yet")
        else:
            st.info("Select an item type to view its visualization")

    # Todo List Tab
    with todos_tab:
        st.header("Todo List")
        
        # Add category filter controls
        if 'todos_df' in st.session_state and not st.session_state.todos_df.empty:
            # Get all unique categories from todos
            all_categories = set()
            for categories in st.session_state.todos_df['categories']:
                all_categories.update(categories)
            
            # Create category filter
            selected_categories = st.multiselect(
                "Filter by Categories",
                sorted(list(all_categories)),
                help="Select one or more categories to filter todos"
            )
            
            # Filter todos based on selected categories
            if selected_categories:
                filtered_todos = st.session_state.todos_df[
                    st.session_state.todos_df['categories'].apply(
                        lambda x: any(cat in x for cat in selected_categories)
                    )
                ]
            else:
                filtered_todos = st.session_state.todos_df
            
            # Sort filtered todos by importance
            filtered_todos = filtered_todos.sort_values('importance', ascending=False)
            
            # Display filtered and sorted todos
            if not filtered_todos.empty:
                for _, todo in filtered_todos.iterrows():
                    with st.expander(f"{todo['title']} (Importance: {todo['importance']})"):
                        st.write(todo['details'])
                        st.write(f"Categories: {', '.join(todo['categories'])}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Edit", key=f"edit_{todo['title']}"):
                                st.session_state.selected_todo = todo['title']
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"delete_{todo['title']}"):
                                if pipeline_service.delete_todo(todo['title']):
                                    st.success(f"Deleted todo '{todo['title']}'")
                                    st.rerun()
            else:
                st.info("No todos found for the selected categories.")
        else:
            st.info("No todos added yet. Use the sidebar to add new todos.")

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
