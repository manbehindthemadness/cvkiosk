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
    matrix_sorter,
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

constants = constants_parser(  # Get screen and geometry constants.
    config['constants'],
)

style = style_parser(  # Get style sheet.
    'tutorial',
    constants
)


mstyle = style['main']
mstyle['_alerts'] = gp.samples.alerts['alert_data']  # Pull sample alert data for the ticker tape.
gui.geometry = mstyle['geometry']  # Configure the UX size.

base = tk.Frame(
    gui,
    width=constants['_screen_width'],
    height=constants['_screen_height'],
    bg=mstyle['background'],
    bd=0,
    highlightthickness=0
)
base.pack(expand=True, fill='both')

layout = layout_uninit(base, cache, config)  # Init the layout.
layout.configure(
    bg=mstyle['background'],
    width=mstyle['price_canvas_width'],
    height=mstyle['price_canvas_height'],
    bd=0,
    highlightthickness=0
)  # Configure the price chart size.


price_matrix = gp.ChartToPix(layout, *mstyle['price_matrix_offsets'])  # Init matrices.
price_matrix.solve(price_data=gp.samples.price_data, increment=mstyle['price_increment'], timequote='1H:BTC/USDT')  # TODO: Build timequote from settings.
matrices = matrix_sorter(price_matrix, dict())
matrices.update({
    '_triggers1': test_o_random(matrices['_cu'], 20),
    '_triggers2': test_o_random(matrices['_cl'], 20),
    '_triggers3': test_o_random(matrices['_ac'], 20),
    '_triggers4': test_o_random(matrices['_cu'], 20),
    '_triggers5': test_o_random(matrices['_cl'], 20),
    '_triggers6': test_o_random(matrices['_cu'], 20),
})

style = matrix_parser(style, matrices)  # Update geometry into style.

if 'ticker' in style.keys():
    t = style['ticker']['style']
    ticker = layout.ticker
    ticker.configure(
        width=constants['_screen_width'],
        height=constants['_screen_height'],
        bg=t['background']
    )
    ticker.place(
        x=t['x'],
        y=t['y']
    )


layout.configure_widgets(style)
layout.draw_widgets()
print('done!')
gui.mainloop()
