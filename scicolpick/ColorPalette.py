from colormath.color_objects import HSLColor, sRGBColor, LabColor, CMYKColor
import colormath.color_conversions as color_conversions
import colormath.color_diff as color_diff
import random
import itertools
from scicolpick.Color import Color


class ColorPalette(object):
    '''
    Color palette with
        0:      black
        1 to n: specified color
        n+1:    white
    '''

    DEBUG = False
    @classmethod
    def p(cls, *a, **kw):
        if cls.DEBUG:
            print(*a, **kw)

    def __init__(self, n):
        self.n = n
        self._colors = [Color(0, 0, 0) for i in range(n)]
        self._black = Color(0, 0, 0)
        self._white = Color(100, 0, 0)

    def colors(self):
        return [self._black] + self._colors + [self._white]

    def color(self, i):
        if i == 0:
            return self._black
        elif i == self.n + 1:
            return self._white
        else:
            return self._colors[i-1]

    def to_hex(self):
        return [self.color(i).to_hex() for i in range(0, self.n + 2)]

    def to_rgb(self):
        return [self.color(i).to_rgb() for i in range(0, self.n + 2)]

    def to_grayhex(self):
        return [self.color(i).to_grayhex() for i in range(0, self.n + 2)]

    def calc_differences(self):
        return [self.color(i).diff(self.color(i+1)) for i in range(self.n + 1)]

    def initialize_with_equalized_gray(self):
        def get_equalized(a, b, c, ab, bc):
            return Color(b.l() + 0.05 * (c.l() - a.l()) * (bc - ab) / (ab + bc), 0, 0)

        # initialize
        self._colors = [Color(100 * i / (self.n + 1), 0, 0) for i in range(1, self.n + 1)]
        matching_criterion = 0.1  # could be something else

        # equalize
        d = self.calc_differences()
        while True:
            self.p(d, self.to_hex())
            done = True
            for i in range(1, self.n + 1):
                if abs(d[i] - d[i-1]) > matching_criterion:
                    done = False
                    self._colors[i-1] = get_equalized(self.color(i-1), self.color(i), self.color(i+1), d[i-1], d[i])
                    d[i-1] = self.color(i).diff(self.color(i-1))
                    d[i] = self.color(i).diff(self.color(i+1))
            if done:
                return self

    def colorize(self):
        [c.colorize() for c in self._colors]
        return self

    def calc_min_distance(self):
        combinations = itertools.combinations(range(self.n + 2), 2)
        distances = [self.color(i).diff(self.color(j)) for i, j in combinations]
        return min(distances)
