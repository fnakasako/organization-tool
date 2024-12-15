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

        # Add main nodes
        G.add_node('c1', text=f"Concern:\n{decision_data['concern']}", node_type='concern')
        G.add_node('q1', text=f"Question:\n{decision_data['question']}", node_type='question')
        G.add_node('d1', text=f"Decision:\n{decision}", node_type='decision')
        G.add_node('r1', text=f"Rationale:\n{decision_data['rationale']}", node_type='rationale')

        # Add basic edges
        G.add_edge('c1', 'q1')
        G.add_edge('q1', 'd1')
        G.add_edge('d1', 'r1')

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