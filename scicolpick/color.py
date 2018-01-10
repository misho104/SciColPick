from colormath.color_objects import sRGBColor, LabColor
import colormath.color_conversions as color_conversions
import colormath.color_diff as color_diff
import random


class Color(object):
    '''
    A wrapper of LabColor. Originally designed as a subclass of LabColor, but implemented as a wrapper
    because convert_color only accepts (and does not accept subclasses of) LabColor.
    '''
    def __init__(self, *args, **kwargs):
        self.c = LabColor(*args, **kwargs)

    def l(self):
        return self.c.lab_l

    def a(self):
        return self.c.lab_a

    def b(self):
        return self.c.lab_b

    def to_rgb(self):
        return color_conversions.convert_color(self.c, sRGBColor)

    def to_hex(self):
        return self.to_rgb().get_rgb_hex()

    def to_grayhex(self):
        rgb = self.to_rgb().get_value_tuple()
        y = self.linear_to_srgb(sum(self.rgb_to_gray_weight[i] * self.srgb_to_linear(rgb[i]) for i in [0,1,2]))
        return sRGBColor(y, y, y).get_rgb_hex()

    def diff(self, other):
        if isinstance(other, LabColor):
            return color_diff.delta_e_cie2000(self.c, other)
        elif isinstance(other, Color):
                return color_diff.delta_e_cie2000(self.c, other.c)
        else:
            return self.diff(color_conversions.convert_color(other.c, LabColor))

    rgb_to_gray_weight = [0.2126, 0.7152, 0.0722]  # in linear space

    @classmethod
    def srgb_to_linear(cls, c):
        return c / 12.92 if c < 0.04045 else ((c + 0.055) / 1.055)**2.4

    @classmethod
    def linear_to_srgb(cls, c):
        return c * 12.92 if c < 0.0031308 else 1.055 * (c**(1 / 2.4)) - 0.055

    @classmethod
    def random_with_fixed_gray(cls, gray):
        '''
        Generate three random number x, y, z in [0,1) that satisfies
            (x, y, z) . rgb_to_gray_weight = gray

        This forms a triangle plane in a three dimensional space; then the value is uniformly given by
            R = r1 X + r2 Y + (1-r1-r2) Z
        with uniform r1 and r2;
            X = (1/0.2126, 0, 0),
            Y = (0, 1/0.7152, 0),
            Z = (0, 0, 1/0.0722).
        '''
        if gray < 0:
            return [0, 0, 0]
        elif gray < cls.rgb_to_gray_weight[2]:  # the minimal value, 0.0722
            while True:
                r1 = random.random()
                r2 = random.random()
                if r1 + r2 < 1:
                    return [r1 * gray / cls.rgb_to_gray_weight[0],
                            r2 * gray / cls.rgb_to_gray_weight[1],
                            (1-r1-r2) * gray / cls.rgb_to_gray_weight[2]]
        elif gray > 1 - cls.rgb_to_gray_weight[2]:
            return [1 - v for v in cls.random_with_fixed_gray(1-gray)]
        else:
            y_min = max(0., (gray - 1 + cls.rgb_to_gray_weight[1]) / cls.rgb_to_gray_weight[1])
            y_max = min(1., gray / cls.rgb_to_gray_weight[1])
            while True:
                z = random.random()
                y = random.uniform(y_min, y_max)
                x = (gray - y * cls.rgb_to_gray_weight[1] - z * cls.rgb_to_gray_weight[2]) / cls.rgb_to_gray_weight[0]
                if not (x < 0 or x > 1):
                    return [x, y, z]

    def colorize(self, gray_l=None):
        '''
        :param gray_l: the value of lab_l when converted to gray
        '''
        # first convert the gray level to sRGB value
        if gray_l is None:
            gray_l = self.l()
        gray_srgb = color_conversions.convert_color(LabColor(gray_l, 0, 0), sRGBColor).rgb_r
        gray_linear = self.srgb_to_linear(gray_srgb)

        random_linear = self.random_with_fixed_gray(gray_linear)
        random_rgb = [self.linear_to_srgb(c) for c in random_linear]
        rgb = sRGBColor(*random_rgb)
        self.c = color_conversions.convert_color(rgb, LabColor)
