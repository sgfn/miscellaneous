import math


def det_3x3(a, b, c):
    return math.fsum((a[0]*b[1], b[0]*c[1], c[0]*a[1], -c[0]*b[1], -a[0]*c[1], -b[0]*a[1]))
