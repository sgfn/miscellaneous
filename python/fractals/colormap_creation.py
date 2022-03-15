import matplotlib.colors

def create_colormap():
    cmap_dict = {
        'red': [
            [0.0, 0.0, 0.0],
            [0.02, 0.0, 0.0],
            [0.04, 1.0, 1.0],
            #[0.1, 0.0, 0.0],
            #[0.5, 0.5, 0.5],
            [1.0, 0.0, 0.0],
        ],
        'green': [
            [0.0, 0.0, 0.0],
            [0.02, 0.0, 0.0],
            [0.04, 1.0, 1.0],
            #[0.1, 0.0, 0.0],
            #[0.5, 0.5, 0.5],
            [1.0, 0.0, 0.0],
        ],
        'blue': [
            [0.0, 0.5, 0.5],
            [0.04, 1.0, 1.0],
            [0.1, 1.0, 1.0],
            #[0.5, 1.0, 1.0],
            [1.0, 0.0, 0.0],
        ],
    }
    newcmp = matplotlib.colors.LinearSegmentedColormap('testmap00', cmap_dict)
    return newcmp

if __name__ == '__main__':
    pass
