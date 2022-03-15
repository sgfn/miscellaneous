import matplotlib.pyplot as plt
import json

from colormap_creation import create_colormap

def mandelbrot_algorithm(x, y, max_it=1_000):
    z = 0
    c = complex(x, y)
    it = 0
    while True:
        z = z ** 2 + c
        it += 1
        if abs(z) < 2 and it < max_it:
            pass
        else:
            break
    return it

def create_canvas(width, height=None):
    if height is None:
        height = width
    canvas = []
    for k in range(height):
        canvas_line = []
        for i in range(width):
            canvas_line.append(0)
        canvas.append(canvas_line)
    return canvas

def mandelbrot_coordinates(width, height=None):
    if height is None:
        height = width
    WIDTH_RANGE = (-2.5, 1)
    HEIGHT_RANGE = (-1, 1)
    point_width = (abs(WIDTH_RANGE[0]) + abs(WIDTH_RANGE[1])) / width
    point_height = (abs(HEIGHT_RANGE[0]) + abs(HEIGHT_RANGE[1])) / height
    coordinates = []
    actual_height = HEIGHT_RANGE[0]
    for k in range(height):
        actual_width = WIDTH_RANGE[0]
        coordinates_line = []
        for i in range(width):
            coordinates_line.append((actual_width, actual_height))
            actual_width += point_width
        actual_height += point_height
        coordinates.append(coordinates_line)
    return coordinates

def show_image(image, colormap=plt.cm.nipy_spectral_r, colorbar=False):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(70, 40))
    ax.set_facecolor('w')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(-2.5, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    
    plt.imshow(image, origin='lower', extent=(-2.5, 1, -1, 1), 
        cmap=colormap, interpolation='nearest')

    if colorbar:
        plt.colorbar()

    # plt.savefig('mdb7000x4000.png', pad_inches=0, bbox_inches='tight')
    plt.imsave('mdb7000x4000_0.png', image, origin='lower', cmap=colormap)
    plt.show()

def dump_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

def load_data(path):
    with open(path) as f:
        container = json.load(f)
    return container

def create_mandelbrot(img_size, max_it=1_000):
    image = create_canvas(img_size)
    coords = mandelbrot_coordinates(img_size)
    for k in range(img_size):
        for i in range(img_size):
            image[k][i] = mandelbrot_algorithm(coords[k][i][0], 
                coords[k][i][1], max_it)
    return image, coords

def update_mandelbrot(img_size, image, coords, last_max_it, max_it):
    for k in range(img_size):
        for i in range(img_size):
            if image[k][i] == last_max_it:
                image[k][i] = mandelbrot_algorithm(coords[k][i][0], 
                    coords[k][i][1], max_it)
    return image

if __name__ == '__main__':
    cmap = create_colormap()
    mbr = load_data('data/mdb_7000x4000_data.json')
    show_image(mbr, cmap)

    # diff_vals = set()
    # for line in mbr:
    #     for val in line:
    #         diff_vals.add(val)
    # print(diff_vals)

    # image_2000_1000 = load_data('data/mandelbrot2000_1000.json')
    # coords_2000 = load_data('data/coords2000.json')
    # image_2000_10000 = update_mandelbrot(2000, image_2000_1000, coords_2000, 
    #     1_000, 10_000)
    # dump_data(image_2000_10000, 'data/mandelbrot2000_10000.json')

    # img_size = 2000
    # image, coords = create_mandelbrot(img_size)
    # dump_data(image, f'data/mandelbrot{img_size}_1000.json')
    # dump_data(coords, f'data/coords{img_size}.json')
    # show_image(image)
    