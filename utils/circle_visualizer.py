import math

class CircleVisualizer:
    def __init__(self):
        self.colors = {
            'concern': '#ff9999',
            'question': '#99ff99',
            'decision': '#9999ff',
            'goal': '#ffff99',
            'task': '#ff99ff'
        }
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
        center_x = width / 2
        center_y = height / 2
        
        # Generate SVG
        svg_content = self._generate_circle_svg(items_sorted, item_type, width, height)
        return svg_content

    def _generate_circle_svg(self, items, item_type, width, height):
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