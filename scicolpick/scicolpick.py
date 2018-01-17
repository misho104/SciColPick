#!/usr/bin/env python

import click
import copy
from scicolpick.ColorPalette import ColorPalette

__version__ = '0.0.1'

@click.command(help='Color picker for scientific plots with SIZE colors.',
               context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-V', '--version')
@click.argument('size', default=4, type=int)
def scicolpick_main(**args):
    best = (0, None)
    history = []
    i = 0
    while True:
        i = i + 1
        d = 0
        palette = ColorPalette(args['size'])
        while d < 25:
            palette.initialize_with_equalized_gray().colorize()
            d = palette.calc_min_distance()
        history.append((d, palette))
        p = copy.deepcopy(palette)
        d = p.maximize().calc_min_distance()
        history.append((d, p))
        test(history, 'result.png', 'result.txt')
        if i == 12:
            exit(0)


import matplotlib.pyplot as pyplot
import matplotlib.patches as patches
def test(palette_list, png_path='result.png', txt_path='result.txt'):
    figure = pyplot.figure()
    axes = pyplot.axes()

    with open(txt_path, 'w') as file:
        file.write('Gray scale: ')
        for j, c in enumerate(palette_list[-1][1].colors()):
            gray = c.to_grayhex()
            file.write(gray + ' ')
            axes.add_patch(patches.Rectangle(xy=(j, 0), width=1, height=1, fc=gray))
        for i, p in enumerate(palette_list):
            file.write('\nColor No.' + str(i) + ': ')
            for j, c in enumerate(p[1].colors()):
                hex = c.to_hex()
                file.write(hex + ' ')
                axes.add_patch(patches.Rectangle(xy=(j, -1-i), width=1, height=1, fc=hex))
            file.write('  (d=' + str(p[0]) + ')')
        file.write('\n')

    pyplot.axis('scaled')
    axes.set_aspect('equal')

    pyplot.savefig(png_path)