import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

# Ambil data dari txt
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


# Ngecek array itu jumlahnya 315 ga
def isMagicSum(arr):
    return np.sum(arr) == 315

#  
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

def showCube(cube_data):
    fig = go.Figure()
    explosion_factor = 1.2  
    gap = 2
    color_map = {0: 'grey', 1: 'skyblue', 2: 'lightgreen', 3: 'gold', 
                 4: 'orange', 5: 'red', 6: 'purple', 7: 'brown', 8: 'black'}

    # Find magic coordinates
    magic_coords = findMagicCoordinates(cube_data)

    for i in range(5):
        for j in range(5):
            for k in range(5):
                x_pos = i * (explosion_factor + gap)
                y_pos = j * (explosion_factor + gap)
                z_pos = k * (explosion_factor + gap)
                match_count = magic_coords.get((i, j, k), 0)
                color = color_map.get(match_count)

                fig.add_trace(go.Mesh3d(
                    x=[x_pos, x_pos + 1, x_pos + 1, x_pos, x_pos, x_pos + 1, x_pos + 1, x_pos],
                    y=[y_pos, y_pos, y_pos + 1, y_pos + 1, y_pos, y_pos, y_pos + 1, y_pos + 1],
                    z=[z_pos, z_pos, z_pos, z_pos, z_pos + 1, z_pos + 1, z_pos + 1, z_pos + 1],
                    color=color,
                    opacity=0.6,
                    alphahull=0,
                    flatshading=True,
                    hoverinfo='text',
                    text=f"Value: {cube_data[i, j, k]} | Matches: {match_count}",
                ))
                fig.add_trace(go.Scatter3d(
                    x=[x_pos + 0.5],
                    y=[y_pos + 0.5],
                    z=[z_pos + 0.5],
                    mode='text',
                    text=[str(cube_data[i, j, k])],
                    textposition="middle center",
                    textfont=dict(size=12, color="black")
                ))

    # Update layout dengan menghilangkan semua elemen koordinat
    fig.update_layout(
        title="5x5x5 Exploded Magic Cube Visualization",
        scene=dict(
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showbackground=False,
                showaxeslabels=False,
                showticklabels=False,  # Menghilangkan label tick
                visible=False  # Hapus summbu x
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showbackground=False,
                showaxeslabels=False,
                showticklabels=False,  # Menghilangkan label tick
                visible=False  # Hapus sumbu y
            ),
            zaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showbackground=False,
                showaxeslabels=False,
                showticklabels=False,  # Menghilangkan label tick
                visible=False  # hapus sumbu z
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        scene_aspectmode='cube',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.show()


def main(data_source):
    cube_data = loadData(data_source)

    for data in cube_data:
        print(data)

    # magic_coords = findMagicCoordinates(cube_data)
    # for coor in magic_coords:
    #     print(coor) 
    # print(magic_coords)
    showCube(cube_data)



main("cube_data.txt")