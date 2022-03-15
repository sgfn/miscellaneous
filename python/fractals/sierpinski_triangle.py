import random

from matplotlib import pyplot as plt

def transformation_1(p):
    x = p[0]
    y = p[1]
    return 0.5*x, 0.5*y

def transformation_2(p):
    x = p[0]
    y = p[1]
    return 0.5*x + 0.5, 0.5*y + 0.5

def transformation_3(p):
    x = p[0]
    y = p[1]
    return 0.5*x + 1, 0.5*y

def transform(p):
    # List of transformation functions
    transformations = [transformation_1, transformation_2, transformation_3]
    t = random.choice(transformations)
    x, y = t(p)
    return x, y

def draw_triangle(n):
    # Start at (0, 0)
    x = [0]
    y = [0]

    x1, y1 = 0, 0
    for i in range(n):
        x1, y1 = transform((x1, y1))
        x.append(x1)
        y.append(y1)
    return x, y

if __name__ == '__main__':
    # Initial point
    p = (0, 0)
    try:
        # n = int(input('Enter the number of points in the triangle: '))
        raise ValueError
    except ValueError:
        n = 100_000
    x, y = draw_triangle(n)
    
    # Plot the points
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(x, y, c=y, cmap=plt.cm.Greens_r, edgecolors='none', s=1)
    plt.title(f'Triangle with {n} points')
    # Remove the axes.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()
    