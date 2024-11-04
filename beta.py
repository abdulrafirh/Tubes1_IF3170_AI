import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

def loadStatesFromFile(filename):
    """
    Load multiple states from a file where states are separated by commas
    Returns a list of numpy arrays, each representing a 5x5x5 cube state
    """
    with open(filename, 'r') as file:
        content = file.read()
        # Split states by comma and clean up whitespace
        states = content.split(',')
        cube_states = []
        
        for state in states:
            # Convert state string to array of numbers
            try:
                numbers = [int(num) for num in state.strip().split()]
                if len(numbers) != 125:
                    raise ValueError(f"Each state must contain exactly 125 numbers. Found {len(numbers)} numbers.")
                # Reshape into 5x5x5 cube
                cube_states.append(np.array(numbers).reshape((5, 5, 5)))
            except ValueError as e:
                print(f"Error processing state: {e}")
                continue
            
        return cube_states

def isMagicSum(arr):
    return np.sum(arr) == 315

def findMagicCoordinates(cube_data):
    magic_coords = defaultdict(int)

    for i in range(5):
        for j in range(5):
            # Checking along Z-axis
            if isMagicSum(cube_data[i, j, :]):
                for k in range(5):
                    magic_coords[(i, j, k)] += 1
            # Checking along Y-axis
            if isMagicSum(cube_data[i, :, j]):
                for k in range(5):
                    magic_coords[(i, k, j)] += 1
            # Checking along X-axis
            if isMagicSum(cube_data[:, i, j]):
                for k in range(5):
                    magic_coords[(k, i, j)] += 1
        
        # XY plane diagonals for each Z level
        if isMagicSum(cube_data[i, range(5), range(5)]):
            for k in range(5):
                magic_coords[(i, k, k)] += 1
        if isMagicSum(cube_data[i, range(5), range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(i, k, 4 - k)] += 1

        # YZ plane diagonals for each X level
        if isMagicSum(cube_data[range(5), i, range(5)]):
            for k in range(5):
                magic_coords[(k, i, k)] += 1
        if isMagicSum(cube_data[range(5), i, range(4, -1, -1)]):
            for k in range(5):
                magic_coords[(k, i, 4 - k)] += 1

        # XZ plane diagonals for each Y level
        if isMagicSum(cube_data[range(5), range(5), i]):
            for k in range(5):
                magic_coords[(k, k, i)] += 1
        if isMagicSum(cube_data[range(5), range(4, -1, -1), i]):
            for k in range(5):
                magic_coords[(k, 4 - k, i)] += 1

    # Space diagonals
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
    def __init__(self, states):
        self.states = states
        self.current_state_idx = 0
        self.explosion_factor = 1.2
        self.gap = 2
        self.color_map = {
            0: '#DCDCDC', 1: '#AFEBFF', 2: '#99BBFF', 3: '#3A41D4', 
            4: '#ACF1C5', 5: '#1CC198', 6: '#5FCB66', 7: '#287417', 
            8: '#FFFA92', 9: '#FFDC50', 10: '#FFDC9F', 11: '#FFAC06', 
            12: '#FFB492', 13: '#FF6D68', 14: '#FF0900', 15: '#9F120D', 
            16: '#440402'
        }
        self.fig = go.Figure()
        self.setup_figure()

    def find_different_cells(self, state1, state2):
        """
        Menemukan koordinat sel yang berbeda antara dua state
        """
        different_coords = []
        for i in range(5):
            for j in range(5):
                for k in range(5):
                    if state1[i,j,k] != state2[i,j,k]:
                        different_coords.append((i,j,k))
        return different_coords

    def create_cube_traces(self, highlight_coords=None):
        traces = []
        current_state = self.states[self.current_state_idx]
        magic_coords = findMagicCoordinates(current_state)

        for i in range(5):
            for j in range(5):
                for k in range(5):
                    x_pos = i * (self.explosion_factor + self.gap)
                    y_pos = j * (self.explosion_factor + self.gap)
                    z_pos = k * (self.explosion_factor + self.gap)
                    
                    # Tentukan warna: kuning jika di-highlight, sesuai magic lines jika tidak
                    if highlight_coords and (i,j,k) in highlight_coords:
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
                        text=f"Value: {current_state[i, j, k]}<br>Magic Lines: {magic_coords.get((i,j,k), 0)}"
                    ))
                    
                    traces.append(go.Scatter3d(
                        x=[x_pos + 0.5],
                        y=[y_pos + 0.5],
                        z=[z_pos + 0.5],
                        mode='text',
                        text=[str(current_state[i, j, k])],
                        textposition="middle center",
                        textfont=dict(size=18, color="black")
                    ))

        return traces

    def setup_figure(self):
        self.fig = go.Figure(data=self.create_cube_traces())
        
        # Buat frames untuk semua state
        frames = []
        for i in range(len(self.states)):
            # Frame normal untuk state saat ini
            self.current_state_idx = i
            frame = go.Frame(
                data=self.create_cube_traces(),
                name=f"state_{i}",
                traces=[i for i in range(250)]
            )
            frames.append(frame)
            
            # Jika bukan state terakhir, tambahkan frame transisi dengan highlight
            if i < len(self.states) - 1:
                different_coords = self.find_different_cells(self.states[i], self.states[i+1])
                
                # Frame dengan highlight kuning
                highlight_frame = go.Frame(
                    data=self.create_cube_traces(highlight_coords=different_coords),
                    name=f"state_{i}_highlight",
                    traces=[i for i in range(250)]
                )
                frames.append(highlight_frame)
        
        # Reset current state
        self.current_state_idx = 0
        
        # Setup slider dengan frame tambahan untuk highlight
        steps = []
        for i in range(len(frames)):
            step = {
                'args': [[frames[i].name], {
                    'frame': {'duration': 0, 'redraw': True},
                    'mode': 'immediate',
                    'transition': {'duration': 0}
                }],
                'label': f"{i//2 + 1}" if i % 2 == 0 else f"{i//2 + 1}h",
                'method': 'animate'
            }
            steps.append(step)

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
            'steps': steps
        }]
        
        # Setup play/pause dengan durasi yang sesuai untuk transisi
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
                        'frame': {'duration': 1000, 'redraw': True},  # Durasi lebih lama untuk melihat highlight
                        'fromcurrent': True,
                        'transition': {'duration': 300},
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
            title=f"5x5x5 Magic Cube States Visualization ({len(self.states)} states)",
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
            margin=dict(l=0, r=0, t=100, b=0)
        )
        
        self.fig.frames = frames

def main(states_file):
    # Load states from file
    print(f"Loading states from {states_file}...")
    cube_states = loadStatesFromFile(states_file)
    print(f"Successfully loaded {len(cube_states)} states")
    
    # Create visualizer and display
    visualizer = CubeVisualizer(cube_states)
    visualizer.fig.show()

if __name__ == "__main__":
    state_file = "cube_data.txt"  # Your states file
    main(state_file)