from geometria import *


class BetterPlot:
    def __init__(self):
        self.clear()

    def clear(self):
        self.scenes = []
        self.points = []
        self.lines = []
        return self

    def add_pts(self, *pts, c='black', s=.5):
        self.points.append(PointsCollection(pts, color=c, s=s))
        return self

    def add_lines(self, *fr_to, c='black', w=.5):
        self.lines.append(LinesCollection(fr_to, color=c, linewidth=w))
        return self

    def add_polygon(self, pts, close=True, draw_pts=True, c='black', c_p='black', w=.5, s=.5):
        self.add_lines(*[ [pts[i], pts[i-1]] for i in range(0 if close else 1, len(pts)) ], c=c, w=w)
        if draw_pts:
            self.add_pts(*pts, c=c_p, s=s)
        return self

    def add_scene(self, pts=None, lines=None):
        pts = [] if pts is None else pts
        lines = [] if lines is None else lines
        self.scenes.append(Scene(pts.copy(), lines.copy()))
        return self

    def save_scene_cls(self):
        self.scenes.append(Scene(self.points.copy(), self.lines.copy()))
        self.points = []
        self.lines = []
        return self

    def set_limits(self, xlim, ylim=None):
        ylim = xlim if ylim is None else ylim
        self.add_pts((xlim[0], ylim[0]), (xlim[1], ylim[1]), c='white', s=0)
        return self

    def set_uniform_scale(self, curr_xlim, curr_ylim):
        x_mid = (curr_xlim[1] + curr_xlim[0]) / 2
        x_span = curr_xlim[1] - x_mid
        y_mid = (curr_ylim[1] + curr_ylim[0]) / 2
        y_span = curr_ylim[1] - y_mid
        if y_span > x_span*1.5:
            x_span = y_span
        else:
            y_span = x_span
        self.add_pts((x_mid-x_span*1.5, y_mid-y_span), (x_mid+x_span*1.5, y_mid+y_span), c='white', s=0)
        return self

    def get_plot(self):
        if self.scenes:
            p = Plot(scenes=self.scenes)
        else:
            p = Plot(points=self.points, lines=self.lines)
        return p


if __name__ == '__main__':
    b = BetterPlot()
    b.add_polygon([(0, 0), (1, 1), (1, 2), (-7, 8), (-8, 0)], c_p='red', s=30)
    b.add_polygon([(1, 0), (2, -3), (4, 5), (4, 6)], c_p='blue', c='green', s=30)
    b.set_limits((-10, 10))
    b.draw()
