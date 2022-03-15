import random

from matplotlib import pyplot as plt, animation

def transformation(p):
    x = p[0]
    y = p[1]
    return y + 1 - (1.4 * x**2), 0.3*x

def transform(p):
    x, y = transformation(p)
    return x, y

def draw_henons(n):
    # Start at (1, 1)
    x = [1]
    y = [1]

    x1, y1 = 1, 1
    for i in range(n):
        x1, y1 = transform((x1, y1))
        x.append(x1)
        y.append(y1)
    return x, y

def create_animation():
    plt.style.use('dark_background')
    fig = plt.figure()
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    xs = []
    ys = []
    graph, = plt.plot(xs, ys, 'o', markersize=1, c='r')

    def animate_henons(i):
        graph.set_data(x[:i+1], y[:i+1])
        return graph

    anim = animation.FuncAnimation(fig, animate_henons, 
        frames=20_001, interval=1)
    plt.show()

if __name__ == '__main__':
    # Initial point
    p = (1, 1)
    n = 20_000
    x, y = draw_henons(n)
    
    create_animation()
    # Plot the points
    # plt.style.use('dark_background')
    # fig, ax = plt.subplots(figsize=(16, 9))
    # cmap_reference = range(n+1)
    # ax.scatter(x, y, c=cmap_reference, cmap=plt.cm.rainbow, s=1)
    # plt.title(f"Henon's function with {n} points")
    # Remove the axes.
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    