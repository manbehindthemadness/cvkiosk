# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

This is full of aptly named test code.
"""
import random
import tkinter as tk
import graphiend as gp
from utils import (
    config,
    style_parser,
    constants_parser,
    layout_parser,
    matrix_parser,
)


def test_o_random(view_arry: list, alerts: int) -> list:
    """
    This creates random alert arrays for testing.
    """
    def rand_val(randstat: float) -> float:
        """
        Throws out a random value from 1-25
        """
        res = 0
        if not random.randint(0, int(randstat)):
            res = random.randint(1, 25)
        return res

    ll = len(view_arry)
    rand_stat = ll / alerts
    sett: list = [0] * ll
    for idx, s in enumerate(sett):
        s = rand_val(rand_stat)
        sett[idx] = s
    return sett


cache = gp.ImgCache().refresh()
gui = tk.Tk()

config = config('settings')  # Grab our settings.

layout_uninit = layout_parser(  # Get layout widgets.
    config['layout']
)

layout = layout_uninit(gui, cache, config)  # Init the layout.

constants = constants_parser(  # Get screen and geometry constants.
    config['constants'],
)

style = style_parser(  # Get style sheet.
    'tutorial',
    constants
)

mstyle = style['main']
price_matrix = gp.ChartToPix(layout, *mstyle['price_matrix_offsets'])  # Init matrices.
price_matrix.solve(price_data=gp.samples.price_data, increment=mstyle['price_increment'], timequote='1H:BTC/USDT')  # TODO: Build timequote from settings.
coords1 = price_matrix.price_matrix[1]
matrices = {
    '_price_matrix': price_matrix,
    '_coords1': coords1,
    '_triggers1': test_o_random(coords1, 20)
}

style = matrix_parser(style, matrices)  # Update geometry into style.

gui.geometry = mstyle['geometry']
base = gp.Diagram(gui)
base.configure(
    width=mstyle['price_canvas_width'],
    height=mstyle['price_canvas_height'],
    bg='orange'  # We do this, as if we properly wrote the style, we won't see it.
)

layout.configure_widgets(style)
print('done!')
