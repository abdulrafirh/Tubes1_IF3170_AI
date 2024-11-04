import numpy as np
import plotly.graph_objects as go
from collections import defaultdict
import random

# Nge load data dari file txt
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

# Ngecek array itu magic sum ga? (315)
def isMagicSum(arr):
    return np.sum(arr) == 315

#  Ngecek Magic sum dari segala arah
def findMagicCoordinates(cube_data):
    magic_coords = defaultdict(int)

    for i in range(5):
        for j in range(5):
            # Sejajar sumbu Z
            if isMagicSum(cube_data[i, j, :]):
                for k in range(5):
                    magic_coords[(i, j, k)] += 1
            # Sejajar sumbu Y
            if isMagicSum(cube_data[i, :, j]):
                for k in range(5):
                    magic_coords[(i, k, j)] += 1
            # Sejajar sumbu X
            if isMagicSum(cube_data[:, i, j]):
                for k in range(5):
                    magic_coords[(k, i, j)] += 1
        
        # Bidang XY untuk tiap level Z
        if isMagicSum(cube_data[i, range(5), range(5)]):
            for k in range(5):
                magic_coords[(i, k, k)] += 1
        if isMagicSum(cube_data[i, range(5), range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(i, k, 4 - k)] += 1

        # Bidang YZ untuk tiap level X
        if isMagicSum(cube_data[range(5), i, range(5)]):
            for k in range(5):
                magic_coords[(k, i, k)] += 1
        if isMagicSum(cube_data[range(5), i, range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(k, i, 4 - k)] += 1

        # Bidang XZ untuk tiap level Y
        if isMagicSum(cube_data[range(5), range(5), i]):
            for k in range(5):
                magic_coords[(k, k, i)] += 1
        if isMagicSum(cube_data[range(5), range(4, -1, -1), i]):
            for k in range(5):
                magic_coords[(k, 4 - k, i)] += 1

    # Diagonal Ruang
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
            0: '#DCDCDC', 1: '#AFEBFF', 2: '#99BBFF', 3: '#3A41D4', 
            4: '#ACF1C5', 5: '#1CC198', 6: '#5FCB66', 7: '#287417', 8: '#FFFA92', 9 : '#FFDC50', 10: '#FFDC9F', 11: '#FFAC06', 12: '#FFB492', 13: '#FF6D68', 14: '#FF0900', 15: '#9F120D', 16: '#440402'
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
                        text=f"Value: {self.cube_data[i, j, k]} \n Matches: {match_count}"
                    ))
                    
                    traces.append(go.Scatter3d(
                        x=[x_pos + 0.5],
                        y=[y_pos + 0.5],
                        z=[z_pos + 0.5],
                        mode='text',
                        text=[str(self.cube_data[i, j, k])],
                        textposition="middle center",
                        textfont=dict(size=18, color="black")  
                    ))

        return traces

    def setup_figure(self):
        self.fig = go.Figure(data=self.create_cube_traces())
        
        # SLider buat animasi
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

        # Tombol play pause
        updatemenus = [{
            'type': 'buttons',
            'showactive': False,
            'x': 0.1,
            'y': 0.05,  
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
            margin=dict(l=0, r=0, t=100, b=0)  # Margin
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
            
            # swap
            self.swap_values(coord1, coord2)
            
            # hasil frame abis swap
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