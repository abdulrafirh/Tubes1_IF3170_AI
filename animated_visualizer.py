import numpy as np
import plotly.graph_objects as go
from collections import defaultdict
import random

def loadData(data_source):
    if isinstance(data_source, str):
        with open(data_source, 'r') as file:
            data = file.read().split()
            numbers = [int(num) for num in data]
    elif isinstance(data_source, (list, np.ndarray)):
        numbers = list(data_source)
    else:
        raise ValueError("Invalid data source. Must be a filename or an array of numbers.")
    
    if len(numbers) != 125 or len(set(numbers)) != 125:
        raise ValueError("Data must contain exactly 125 unique numbers.")
    
    return np.array(numbers).reshape((5, 5, 5))

def isMagicSum(arr):
    return np.sum(arr) == 315

def findMagicCoordinates(cube_data):
    magic_coords = defaultdict(int)

    for i in range(5):
        for j in range(5):
            if isMagicSum(cube_data[i, j, :]):
                for k in range(5):
                    magic_coords[(i, j, k)] += 1
            if isMagicSum(cube_data[i, :, j]):
                for k in range(5):
                    magic_coords[(i, k, j)] += 1
            if isMagicSum(cube_data[:, i, j]):
                for k in range(5):
                    magic_coords[(k, i, j)] += 1

        if isMagicSum(cube_data[i, range(5), range(5)]):
            for k in range(5):
                magic_coords[(i, k, k)] += 1
        if isMagicSum(cube_data[i, range(5), range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(i, k, 4 - k)] += 1
        if isMagicSum(cube_data[range(5), i, range(5)]):
            for k in range(5):
                magic_coords[(k, i, k)] += 1
        if isMagicSum(cube_data[range(5), i, range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(k, i, 4 - k)] += 1
        if isMagicSum(cube_data[range(5), range(5), i]):
            for k in range(5):
                magic_coords[(k, k, i)] += 1
        if isMagicSum(cube_data[range(5), range(4, -1, -1), i]):
            for k in range(5):
                magic_coords[(k, 4 - k, i)] += 1

    if isMagicSum(cube_data[range(5), range(5), range(5)]):
        for k in range(5):
            magic_coords[(k, k, k)] += 1
    if isMagicSum(cube_data[range(5), range(5), range(4, -1, -1)]):
        for k in range(5):
            magic_coords[(k, k, 4 - k)] += 1
    if isMagicSum(cube_data[range(5), range(4, -1, -1), range(5)]):
        for k in range(5):
            magic_coords[(k, 4 - k, k)] += 1
    if isMagicSum(cube_data[range(5), range(4, -1, -1), range(4, -1, -1)]):
        for k in range(5):
            magic_coords[(k, 4 - k, 4 - k)] += 1

    return magic_coords

class CubeVisualizer:
    def __init__(self, initial_cube_data):
        self.cube_data = initial_cube_data.copy()
        self.explosion_factor = 1.2
        self.gap = 2
        self.color_map = {
            0: '#F0F0F0', 1: '#A9A9A9', 2: '#B5B5B5', 3: '#98D7FF', 
            4: '#74EDDD', 5: '#5DFC8C', 6: '#DEFD6F', 7: '#F5F828', 8: '#FFB829', 9 : '#FF9368', 10: '#FF8888', 11: '#FF1E1E', 12: '#871010', 13: '#871010', 14: '#871010', 15: '#871010', 16: '#871010'
        }
        self.fig = go.Figure()
        self.setup_figure()

    def create_cube_traces(self, highlight_coords=None):
        traces = []
        magic_coords = findMagicCoordinates(self.cube_data)

        for i in range(5):
            for j in range(5):
                for k in range(5):
                    x_pos = i * (self.explosion_factor + self.gap)
                    y_pos = j * (self.explosion_factor + self.gap)
                    z_pos = k * (self.explosion_factor + self.gap)
                    
                    if highlight_coords and (i, j, k) in highlight_coords:
                        color = 'yellow'
                    else:
                        match_count = magic_coords.get((i, j, k), 0)
                        color = self.color_map.get(match_count, 'grey')

                    traces.append(go.Mesh3d(
                        x=[x_pos, x_pos + 1, x_pos + 1, x_pos, x_pos, x_pos + 1, x_pos + 1, x_pos],
                        y=[y_pos, y_pos, y_pos + 1, y_pos + 1, y_pos, y_pos, y_pos + 1, y_pos + 1],
                        z=[z_pos, z_pos, z_pos, z_pos, z_pos + 1, z_pos + 1, z_pos + 1, z_pos + 1],
                        color=color,
                        opacity=0.6,
                        alphahull=0,
                        flatshading=True,
                        hoverinfo='text',
                        text=f"Value: {self.cube_data[i, j, k]}"
                    ))
                    
                    traces.append(go.Scatter3d(
                        x=[x_pos + 0.5],
                        y=[y_pos + 0.5],
                        z=[z_pos + 0.5],
                        mode='text',
                        text=[str(self.cube_data[i, j, k])],
                        textposition="middle center",
                        textfont=dict(size=18, color="black")  # Increased text size to 18px
                    ))

        return traces

    def setup_figure(self):
        self.fig = go.Figure(data=self.create_cube_traces())
        
        # Create slider specifications
        sliders = [{
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 16},
                'prefix': 'State: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 0},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': []
        }]

        # Create play button specifications - now positioned above slider
        updatemenus = [{
            'type': 'buttons',
            'showactive': False,
            'x': 0.1,
            'y': 0.05,  # Positioned just above slider
            'xanchor': 'left',
            'yanchor': 'top',
            'buttons': [
                {
                    'label': '▶️ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 0},
                        'mode': 'immediate',
                    }]
                },
                {
                    'label': '⏸️ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }]

        self.fig.update_layout(
            title="5x5x5 Magic Cube Visualization",
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showline=False, 
                          showbackground=False, showaxeslabels=False, 
                          showticklabels=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, showline=False, 
                          showbackground=False, showaxeslabels=False, 
                          showticklabels=False, visible=False),
                zaxis=dict(showgrid=False, zeroline=False, showline=False, 
                          showbackground=False, showaxeslabels=False, 
                          showticklabels=False, visible=False),
                bgcolor='rgba(0,0,0,0)'
            ),
            scene_aspectmode='cube',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            sliders=sliders,
            updatemenus=updatemenus,
            margin=dict(l=0, r=0, t=100, b=0)  # Adjusted margins for better layout
        )

    def swap_values(self, coord1, coord2):
        i1, j1, k1 = coord1
        i2, j2, k2 = coord2
        self.cube_data[i1, j1, k1], self.cube_data[i2, j2, k2] = \
            self.cube_data[i2, j2, k2], self.cube_data[i1, j1, k1]

    def process_swaps(self, swap_sequence):
        frames = []
        slider_steps = []
        
        # Add initial state
        frames.append(go.Frame(
            data=self.create_cube_traces(),
            name=f"state_0",
            traces=[i for i in range(250)]
        ))
        
        slider_steps.append({
            'args': [['state_0'],
                    {'frame': {'duration': 0, 'redraw': True},
                     'mode': 'immediate',
                     'transition': {'duration': 0}}],
            'label': '0',
            'method': 'animate'
        })

        for idx, swap in enumerate(swap_sequence, 1):
            coord1 = (swap[0][0], swap[0][1], swap[0][2])
            coord2 = (swap[1][0], swap[1][1], swap[1][2])
            
            # Frame highlighting cubes to be swapped
            frames.append(go.Frame(
                data=self.create_cube_traces(highlight_coords={coord1, coord2}),
                name=f"state_{idx*2-1}",
                traces=[i for i in range(250)]
            ))
            
            slider_steps.append({
                'args': [[f"state_{idx*2-1}"],
                        {'frame': {'duration': 0, 'redraw': True},
                         'mode': 'immediate',
                         'transition': {'duration': 0}}],
                'label': f'{idx*2-1}',
                'method': 'animate'
            })
            
            # Perform the swap
            self.swap_values(coord1, coord2)
            
            # Frame showing result after swap
            frames.append(go.Frame(
                data=self.create_cube_traces(),
                name=f"state_{idx*2}",
                traces=[i for i in range(250)]
            ))
            
            slider_steps.append({
                'args': [[f"state_{idx*2}"],
                        {'frame': {'duration': 0, 'redraw': True},
                         'mode': 'immediate',
                         'transition': {'duration': 0}}],
                'label': f'{idx*2}',
                'method': 'animate'
            })

        self.fig.frames = frames
        self.fig.layout.sliders[0].steps = slider_steps
        return self.fig

def generate_random_swap_sequence(n_swaps=20, cube_size=5):
    swap_sequence = []
    for _ in range(n_swaps):
        x1 = random.randint(0, cube_size-1)
        y1 = random.randint(0, cube_size-1)
        z1 = random.randint(0, cube_size-1)
        val1 = random.randint(1, 125)
        
        while True:
            x2 = random.randint(0, cube_size-1)
            y2 = random.randint(0, cube_size-1)
            z2 = random.randint(0, cube_size-1)
            if not (x1 == x2 and y1 == y2 and z1 == z2):
                break
        val2 = random.randint(1, 125)
        
        swap_sequence.append([(x1,y1,z1,val1), (x2,y2,z2,val2)])
    
    return swap_sequence

def main(data_source):
    cube_data = loadData(data_source)
    swap_sequence = generate_random_swap_sequence(20)
    
    print("Swap Sequence:")
    for i, swap in enumerate(swap_sequence, 1):
        print(f"Swap {i}: {swap}")
    
    visualizer = CubeVisualizer(cube_data)
    fig = visualizer.process_swaps(swap_sequence)
    fig.show()

if __name__ == "__main__":
    main("cube_data.txt")