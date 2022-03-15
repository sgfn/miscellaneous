'''
Program calculating escape iteration values for points of the Mandelbrot set.
'''

import json

import matplotlib.pyplot as plt

from colormap_creation import create_colormap

def load_json(path):
    '''Helper function loading data from a specified json file.'''
    with open(path) as f:
        data = json.load(f)
    return data

def dump_json(data, path, mode='a'):
    '''
    Helper function dumping data to a specified json file.
    Use mode='a' to append, 'w' to (over)write.
    '''
    with open(path, mode) as f:
        json.dump(data, f)

def points_calc(grid_width, grid_height=None, 
    width_limits=(-2.5, 1), height_limits=(-1, 1)):
    '''
    Function calculating exact width and height values of a single point (pixel)
    in the specified canvas.
    '''
    # Do not use - returns values prone to float storing errors (values 
    # require rounding)
    if grid_height is None:
        grid_height = grid_width
    width = abs(width_limits[0]) + abs(width_limits[1])
    height = abs(height_limits[0]) + abs(height_limits[1])

    point_width = width / grid_width
    point_height = height / grid_height

    return point_width, point_height

def create_dataspace(width, height=None, 
    width_limits=(-2.5, 1), height_limits=(-1, 1)):
    '''Function creating a list with the x and y values of each point.'''
    # Do not use - a better approach is to calculate the values on the go,
    # as that requires less memory
    if height is None:
        height = width
    p_width, p_height = points_calc(width, height)
    canvas = []
    for k in range(height):
        canvas_line = []
        for i in range(width):
            canvas_line.append(
                [round(width_limits[0] + i*p_width, 3), 
                    round(height_limits[0] + k*p_height, 3)]
            )
        canvas.append(canvas_line)
    return canvas

def mandelbrot_algorithm(x, y, max_it=1_000, verbose=False, detect_loops=True):
    '''
    Function calculating escape iteration values (up to max_it=1000 by default) 
    for the specified (x, y) point.
    Will detect loops by default (and stop iterating once it does, returning
    the maximal value max_it), this can be suppressed by setting 
    detect_loops=False.
    Set verbose=True to toggle feedback to console, not recommended for large 
    quantities of points being checked.
    '''
    # Define variables z, c and it
    z = 0
    c = complex(x, y)
    it = 0
    # If flag verbose is set, communicate what is happening
    if verbose:
        print(f"Calculating values for starting point ({x}, {y}):")
        print(f"z={z} c={c}")
    # If flag detect_loops is set, keep unique values of z to see when they
    # start to form a loop
    if detect_loops:
        z_values = set()
        z_values.add(z)

    # Main loop to calculate escape value of a point (up to max_it)
    while True:
        z = z ** 2 + c
        it += 1
        # If verbose, print present values of variables
        if verbose:
            print(f"it={it} z={z} |z|={abs(z)}")

        if detect_loops:
            # Compare lengths of z_values before and after adding z to see
            # whether it is already a part of the set
            z_set_length = len(z_values)
            z_values.add(z)
            if z_set_length == len(z_values):
                # If verbose, print information about the loop
                if verbose:
                    print(f"Loop start detected at it={it}")
                # Return the maximum iteration value specified
                return max_it

        if abs(z) < 2 and it < max_it:
            pass
        else:
            break
    return it

def create_mandelbrot(width, height):
    '''
    Function creating a json file with iteration values for points of 
    the Mandelbrot set. Use width, height to specify the amount of pixels.
    '''
    # Setup the x and y values of the first point
    x_initial = -2.5
    y_initial = -1.0
    x = x_initial
    y = y_initial

    # Setup vertical and horizontal increment values for each subsequent point
    x_increment = 0.0005
    y_increment = 0.0005

    # Create an empty list for all the data
    data = []

    # Fill the list. We're using height/2+1 because the Mandelbrot set is 
    # symmetrical with respect to the real (horizontal) axis.
    # Using simply height/2 omits calculations for points on the x axis (y=0)
    for k in range(int(height/2)+1):
        # Write the column number we're on in console
        print(f"COL {k+1}/{int(height/2)+1}")
        # Create an empty row to store the values
        data_row = []
        for i in range(width):
            # Calculate the escape iteration value and store it
            data_row.append(mandelbrot_algorithm(x, y))
            # Increment the x value for the next point
            x += x_increment
        # Store the values of the entire row
        data.append(data_row)
        # Setup the x and y values for the first point in the next column
        x = x_initial
        y += y_increment
    
    # Fill the rest of the list (symmetry with respect to the real axis)
    for k in range(int(height/2)-1, -1, -1):
        data.append(data[k])
    
    return data

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
    # USE IMSAVE, NOT SAVEFIG
    # plt.savefig('mdb7000x4000.png', pad_inches=0, bbox_inches='tight')
    # plt.imsave('mdb7000x4000_0.png', image, origin='lower', cmap=colormap)
    plt.show()

def get_user_input():
    available_modes = {
        'create': 'Create a set and export it to a JSON file',
        'display': 'Display set from JSON file',
    }
    aliases = {
        'create': 'create',
        'display': 'display',
        'c': 'create',
        'd': 'display',
        '': 'display',
    }
    print('\nAvailable modes: ')
    for key, value in available_modes.items():
        print(f'{key} - {value}')
    mode = input('\nChoose a mode (default: display): ')
    if mode not in aliases.keys():
        print(f"'{mode}' is not recognized as an available mode.")
        return get_user_input()

    if aliases[mode] == 'create':
        width = 7000
        height = 4000

        message = f'Calculating values for canvas of size {width}x{height},\n'
        message += f'beginning at (-2.5, -1) and ending at (1, 1),\nwith the '
        message += f'max iteration value set to 1000.'
        print(message)

        # Calculate the values of the Mandelbrot set
        data = create_mandelbrot(width, height)
        # Set path of the file to which we're writing
        path = f'data/NEW_mdb_{width}x{height}_data.json'
        print(f'Creation succesful. Exporting to {path}')
        # Export the values to a JSON file
        dump_json(data, path, 'w')
    else:
        val = input('Use own colormap? (n to deny, anything else to approve): ')
        if val == 'n':
            cmap = plt.cm.nipy_spectral_r
        else:
            cmap = create_colormap()
        
        path = 'data/mdb_7000x4000_data.json'
        mbr_set = load_json(path)
        print(f'Loading and displaying image from {path}.')
        show_image(mbr_set, cmap)  

def test_values():
    width = 70
    height = 40
    x_start = -2.5
    x_end = 1
    y_start = -1
    y_end = 1
    x_span = abs(x_start) + abs(x_end)
    y_span = abs(y_start) + abs(y_end)
    x_increment = x_span/width
    y_increment = y_span/height
    print(f'width: {width}')
    print(f'height: {height}')
    print(f'x increment: {x_increment}')
    print(f'y increment: {y_increment}')
    digits = 0
    while True:
        x_increment_rounded = round(x_increment, digits)
        if x_increment_rounded == x_increment:
            break
        digits += 1
    x_precision = digits
    digits = 0
    while True:
        y_increment_rounded = round(y_increment, digits)
        if y_increment_rounded == y_increment:
            break
        digits += 1
    y_precision = digits
    print(f'x precision: {x_precision}')
    print(f'y precision: {y_precision}')
    print('\nx values:')
    x = x_start
    y = y_start
    for i in range(width):
        print(round(x, x_precision))
        x += x_increment_rounded
    print('\ny values:')
    for i in range(height):
        print(round(y, y_precision))
        y += y_increment_rounded

if __name__ == '__main__':
    get_user_input()
    # val = mandelbrot_algorithm(-0.301, 0.1356, verbose=True)
    # print(f'ANSWER: {val}')
    