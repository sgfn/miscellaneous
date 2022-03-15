import random

from matplotlib import pyplot as plt

def transformation_1(p):
    # 0.85 probability
    x = p[0]
    y = p[1]
    return 0.85*x + 0.04*y, -0.04*x + 0.85*y + 1.6

def transformation_2(p):
    # 0.07 probability
    x = p[0]
    y = p[1]
    return 0.2*x - 0.26*y, 0.23*x + 0.22*y + 1.6

def transformation_3(p):
    # 0.07 probability
    x = p[0]
    y = p[1]
    return -0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44

def transformation_4(p):
    # 0.01 probability
    x = p[0]
    y = p[1]
    return 0, 0.16*y

def get_index(probability):
    r = random.random()
    c_probability = 0
    sum_probability = []
    for p in probability:
        c_probability += p
        sum_probability.append(c_probability)
    for item, sp in enumerate(sum_probability):
        if r <= sp:
            return item
    return len(probability)-1

def transform(p):
    # List of transformation functions
    transformations = [transformation_1, transformation_2, transformation_3,
        transformation_4]
    probability = [0.85, 0.07, 0.07, 0.01]
    # Pick a random transformation function and call it
    tindex = get_index(probability)
    t = transformations[tindex]
    x, y = t(p)
    return x, y

def draw_fern(n):
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
        # n = int(input('Enter the number of points in the Fern (def 10000): '))
        raise ValueError
    except ValueError:
        n = 100_000
    x, y = draw_fern(n)
    
    # Plot the points
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(x, y, c=x, cmap=plt.cm.winter, s=1)
    plt.title(f'Fern with {n} points')
    # Remove the axes.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.show()
    