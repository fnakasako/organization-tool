import streamlit as st
import networkx as nx
from io import StringIO
import math

class BaseVisualizer:
    def __init__(self):
        self.colors = {
            'concern': '#ff9999',    # Light red
            'question': '#99ff99',   # Light green
            'decision': '#9999ff',   # Light blue
            'rationale': '#ffcc99',  # Light orange
            'goal': '#ffff99',       # Light yellow
            'task': '#ff99ff'        # Light purple
        }
        
class GraphVisualizer(BaseVisualizer):
    def __init__(self, pipeline_service=None, graph_service=None):
        super().__init__()
        self.pipeline_service = pipeline_service
        self.graph_service = graph_service
        self.node_radius = 80
        self.text_padding = 10

    def display_graph(self, G):
        """Original interface method for backwards compatibility"""
        if not G:
            return None

        pos = self._calculate_positions(G)
        dimensions = self._calculate_graph_dimensions(G, pos)
        svg_content = self._generate_svg(G, pos, dimensions)
        return svg_content


    def render(self):
        raise NotImplementedError("Subclasses must implement render method")
        
class PipelineVisualizer(BaseVisualizer):
    def __init__(self, pipeline_service, graph_service):
        super().__init__()
        self.pipeline_service = pipeline_service
        self.graph_service = graph_service
        self.node_radius = 80
        self.text_padding = 10

    def render(self, selected_decision):
        """Render the pipeline visualization for a selected decision"""
        graph = self.graph_service.generate_decision_graph(selected_decision)
        svg_content = self._generate_visualization(graph)
        if svg_content:
            self._render_interactive_svg(svg_content)

    def _generate_visualization(self, G):
        """Generate the complete visualization"""
        if not G:
            return None

        pos = self._calculate_positions(G)
        dimensions = self._calculate_graph_dimensions(G, pos)
        return self._generate_svg(G, pos, dimensions)

    def _calculate_positions(self, G):
        """Calculate node positions for triangular layout"""
        pos = {}
        
        # Canvas dimensions
        canvas_width = 1200
        canvas_height = 800
        base_y = canvas_height - 100  # Bottom of triangle
        peak_y = 100                  # Top of triangle
        
        # Core triangle positions
        pos['c1'] = (200, base_y)                    # Concern (bottom left)
        pos['q1'] = (canvas_width/2, base_y - 200)   # Question (middle)
        pos['d1'] = (canvas_width/2, peak_y)         # Decision (top)
        pos['r1'] = (canvas_width/2, peak_y + 150)   # Rationale (below decision)

        # Get goals and tasks
        goals = [n for n in G.nodes() if G.nodes[n]['node_type'] == 'goal']
        
        if goals:
            goal_count = len(goals)
            goal_spacing = (base_y - peak_y) / (goal_count + 1)
            
            for i, goal in enumerate(goals):
                # Position goals along right diagonal
                goal_y = peak_y + ((i + 1) * goal_spacing)
                goal_x = canvas_width - 300 + (((base_y - goal_y) / (base_y - peak_y)) * 100)
                pos[goal] = (goal_x, goal_y)
                
                # Position related tasks
                goal_tasks = [n for n in G.nodes() if (
                    G.nodes[n]['node_type'] == 'task' and 
                    goal in G.predecessors(n)
                )]
                
                if goal_tasks:
                    task_spacing = 100
                    for j, task in enumerate(goal_tasks):
                        task_y = goal_y + (j - len(goal_tasks)/2) * task_spacing
                        pos[task] = (canvas_width - 100, task_y)

        return pos

    def _calculate_graph_dimensions(self, G, pos):
        """Calculate overall graph dimensions"""
        min_x = min(p[0] for p in pos.values())
        max_x = max(p[0] for p in pos.values())
        min_y = min(p[1] for p in pos.values())
        max_y = max(p[1] for p in pos.values())
        
        width = (max_x - min_x) * 1.5
        height = (max_y - min_y) * 1.5
        
        return {
            'width': max(width, 1000),
            'height': max(height, 800),
            'view_box': f"{min_x-100} {min_y-100} {width+200} {height+200}"
        }

    def _generate_svg(self, G, pos, dimensions):
        """Generate SVG content for the graph"""
        output = StringIO()
        
        # SVG header
        output.write(self._get_svg_header(dimensions))
        
        # Draw edges
        self._draw_edges(G, pos, output)
        
        # Draw nodes
        self._draw_nodes(G, pos, output)
        
        # Add arrowhead definition and close SVG
        output.write(self._get_svg_footer())
        
        return output.getvalue()

    def _get_svg_header(self, dimensions):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" 
                    width="{dimensions['width']}" 
                    height="{dimensions['height']}"
                    viewBox="{dimensions['view_box']}"
                    style="background-color: white;">
                    <defs>
                        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                            <feOffset dx="2" dy="2"/>
                            <feComponentTransfer>
                                <feFuncA type="linear" slope="0.3"/>
                            </feComponentTransfer>
                            <feMerge>
                                <feMergeNode/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                    </defs>
                    <g class="zoom-pan-group">'''

    def _draw_edges(self, G, pos, output):
        for edge in G.edges():
            start = pos[edge[0]]
            end = pos[edge[1]]
            ctrl_x = (start[0] + end[0]) / 2
            ctrl_y = (start[1] + end[1]) / 2 - 30
            path = f"M {start[0]},{start[1]} Q {ctrl_x},{ctrl_y} {end[0]},{end[1]}"
            output.write(f'''<path d="{path}" 
                           stroke="gray" 
                           stroke-width="2" 
                           fill="none" 
                           marker-end="url(#arrowhead)"/>''')

    def _draw_nodes(self, G, pos, output):
        for node in G.nodes():
            node_type = G.nodes[node]['node_type']
            text = G.nodes[node]['text']
            x, y = pos[node]
            
            output.write(f'''<g transform="translate({x},{y})" class="node" filter="url(#shadow)">
                            <circle r="{self.node_radius}"
                                   fill="{self.colors[node_type]}"
                                   stroke="#666"
                                   stroke-width="1"/>''')
            
            text_width = self.node_radius * 1.8
            output.write(self._get_node_text(text, text_width))
            output.write('</g>')

    def _get_node_text(self, text, text_width):
        return f'''<foreignObject 
                    x="{-text_width/2}" 
                    y="{-self.node_radius}"
                    width="{text_width}" 
                    height="{self.node_radius * 2}">
                    <div xmlns="http://www.w3.org/1999/xhtml"
                         style="font-family: Arial; 
                                font-size: 14px;
                                padding: {self.text_padding}px;
                                width: 100%;
                                height: 100%;
                                overflow: hidden;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                text-align: center;">
                        {text}
                    </div>
                </foreignObject>'''

    def _get_svg_footer(self):
        return '''<defs>
                    <marker id="arrowhead" 
                            viewBox="0 0 10 10" 
                            refX="20" 
                            refY="5"
                            markerWidth="6" 
                            markerHeight="6"
                            orient="auto">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="gray"/>
                    </marker>
                </defs>
                </g></svg>'''

    def _render_interactive_svg(self, svg_content):
        """Render SVG with interactive features"""
        st.components.v1.html(
            f'''
            <div style="width: 100%; overflow: auto; border: 1px solid #ccc; border-radius: 5px;">
                {svg_content}
            </div>
            <script>
                {self._get_interactive_js()}
            </script>
            <style>
                svg {{
                    cursor: grab;
                }}
                svg:active {{
                    cursor: grabbing;
                }}
            </style>
            ''',
            height=600
        )

    @staticmethod
    def _get_interactive_js():
        return '''
            const svg = document.querySelector('svg');
            const zoomGroup = svg.querySelector('.zoom-pan-group');
            let scale = 1;
            let pointX = 0;
            let pointY = 0;
            let start = { x: 0, y: 0 };
            
            svg.addEventListener('wheel', (event) => {
                event.preventDefault();
                const delta = event.deltaY;
                const scaleAmount = delta > 0 ? 0.9 : 1.1;
                const pt = svg.createSVGPoint();
                pt.x = event.clientX;
                pt.y = event.clientY;
                const svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
                scale *= scaleAmount;
                pointX = svgP.x + (pointX - svgP.x) * scaleAmount;
                pointY = svgP.y + (pointY - svgP.y) * scaleAmount;
                zoomGroup.setAttribute('transform', 
                    `translate(${pointX}, ${pointY}) scale(${scale})`);
            });

            svg.addEventListener('mousedown', (event) => {
                if (event.button === 0) {
                    start = { x: event.clientX - pointX, y: event.clientY - pointY };
                    svg.addEventListener('mousemove', drag);
                    svg.addEventListener('mouseup', endDrag);
                }
            });

            function drag(event) {
                pointX = event.clientX - start.x;
                pointY = event.clientY - start.y;
                zoomGroup.setAttribute('transform', 
                    `translate(${pointX}, ${pointY}) scale(${scale})`);
            }

            function endDrag() {
                svg.removeEventListener('mousemove', drag);
                svg.removeEventListener('mouseup', endDrag);
            }

            // Touch support
            let touchStart = null;
            let lastTouchDistance = 0;

            svg.addEventListener('touchstart', (event) => {
                if (event.touches.length === 2) {
                    event.preventDefault();
                    touchStart = {
                        x: (event.touches[0].clientX + event.touches[1].clientX) / 2,
                        y: (event.touches[0].clientY + event.touches[1].clientY) / 2
                    };
                    lastTouchDistance = Math.hypot(
                        event.touches[0].clientX - event.touches[1].clientX,
                        event.touches[0].clientY - event.touches[1].clientY
                    );
                }
            });

            svg.addEventListener('touchmove', (event) => {
                if (event.touches.length === 2) {
                    event.preventDefault();
                    const touchDistance = Math.hypot(
                        event.touches[0].clientX - event.touches[1].clientX,
                        event.touches[0].clientY - event.touches[1].clientY
                    );
                    const scaleAmount = touchDistance / lastTouchDistance;
                    lastTouchDistance = touchDistance;
                    scale *= scaleAmount;
                    const currentTouchCenter = {
                        x: (event.touches[0].clientX + event.touches[1].clientX) / 2,
                        y: (event.touches[0].clientY + event.touches[1].clientY) / 2
                    };
                    pointX += currentTouchCenter.x - touchStart.x;
                    pointY += currentTouchCenter.y - touchStart.y;
                    touchStart = currentTouchCenter;
                    zoomGroup.setAttribute('transform', 
                        `translate(${pointX}, ${pointY}) scale(${scale})`);
                }
            });
        '''
        
class CircleVisualizer(BaseVisualizer):
    def __init__(self):
        super().__init__()
        self.base_radius = 30
        self.padding = 10

    def create_circle_graph(self, items, item_type):
        """Create an SVG circle graph where circle sizes are based on urgency"""
        if not items:
            return None

        # Sort items by urgency for better layout
        items_sorted = sorted(items, key=lambda x: x['urgency'], reverse=True)
        
        # Calculate layout
        width = 800
        height = 600
        
        # Generate SVG
        return self._generate_circle_svg(items_sorted, item_type, width, height)

    def _generate_circle_svg(self, items, item_type, width, height):
        """Generate SVG content for the circle visualization"""
        output = []
        output.append(f'''
            <svg xmlns="http://www.w3.org/2000/svg" 
                width="{width}" height="{height}"
                style="background-color: white;">
            <defs>
                <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
                    <feOffset dx="2" dy="2"/>
                    <feComponentTransfer>
                        <feFuncA type="linear" slope="0.3"/>
                    </feComponentTransfer>
                    <feMerge>
                        <feMergeNode/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
        ''')

        # Calculate positions in a spiral layout
        positions = self._calculate_spiral_positions(items, width, height)

        # Draw circles
        for item, pos in zip(items, positions):
            radius = self.base_radius * (item['urgency'] / 50)  # Scale radius by urgency
            x, y = pos
            
            # Create circle with text
            output.append(f'''
                <g transform="translate({x},{y})" filter="url(#shadow)">
                    <circle r="{radius}"
                           fill="{self.colors[item_type]}"
                           stroke="#666"
                           stroke-width="1"/>
                    <foreignObject x="{-radius}" y="{-radius}"
                                 width="{radius*2}" height="{radius*2}">
                        <div xmlns="http://www.w3.org/1999/xhtml"
                             style="width: 100%;
                                    height: 100%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    text-align: center;
                                    font-family: Arial;
                                    font-size: {max(10, radius/4)}px;
                                    overflow: hidden;">
                            <div style="padding: 5px;">
                                {item[item_type]}<br/>
                                <small>Urgency: {item['urgency']}</small>
                            </div>
                        </div>
                    </foreignObject>
                </g>
            ''')

        output.append('</svg>')
        return '\n'.join(output)

    def _calculate_spiral_positions(self, items, width, height):
        """Calculate positions for circles in a spiral pattern"""
        positions = []
        center_x = width / 2
        center_y = height / 2
        
        # Use golden ratio for spiral
        golden_ratio = (1 + math.sqrt(5)) / 2
        
        for i in range(len(items)):
            # Calculate spiral coordinates
            angle = i * golden_ratio * 2 * math.pi
            radius = 20 * math.sqrt(i)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions.append((x, y))
            
        return positions