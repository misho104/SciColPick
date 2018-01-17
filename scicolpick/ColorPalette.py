import itertools, functools
from scicolpick.Color import Color, ColorRangeError
import numpy as np
from scipy.optimize import minimize

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
        self._vector = None

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

    def colorize(self, grays=None, vector=None):
        if grays is None:
            grays = [None for c in self._colors]

        if vector is None:
            [c.colorize(grays[i]) for i, c in enumerate(self._colors)]
            self._vector = np.array(functools.reduce(lambda s, e: s + list(e), [c.vector for c in self._colors], []))
        else:
            v = vector.reshape(self.n, 2)
            [c.colorize(grays[i], tuple(v[i])) for i, c in enumerate(self._colors)]
        return self

    def calc_min_distance(self):
        combinations = itertools.combinations(range(self.n + 2), 2)
        distances = [self.color(i).diff(self.color(j)) for i, j in combinations]
        return min(distances)

    def maximize(self):
        # Gray level is gradually modified due to numerical precision. so memorize the first gray level.
        grays = [c.l() for c in self._colors]
        self.temp = (self._vector, 0)
        def f(x):
            try:
                self.colorize(grays, x)
            except ColorRangeError:
                return 99999
            d = (-1) * self.calc_min_distance()
            if d < self.temp[1]:
                self.temp = (x, d)
            return d

        if self._vector is None:
            self.colorize(grays)

        minimize(f, self._vector, method='nelder-mead',
                    options={'disp': True, 'maxiter': 1000, 'maxfev': 1000})
        self.colorize(grays, self.temp[0])
        self.temp = None
        return self
