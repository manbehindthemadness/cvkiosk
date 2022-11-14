# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------

This is full of aptly named test code.
"""
import tkinter as tk
import graphiend as gp
from utils import (
    config,
    style_parser,
    constants_parser,
    layout_parser,
    matrix_parser,
    matrix_sorter,
    test_o_random,
)


cache = gp.ImgCache().refresh()
gui = tk.Tk()

config = config('settings')  # Grab our settings.

# noinspection DuplicatedCode
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
    '_triggers1': test_o_random(matrices['_cu'], 5),
    '_triggers2': test_o_random(matrices['_cl'], 5),
    '_triggers3': test_o_random(matrices['_ac'], 5),
    '_triggers4': test_o_random(matrices['_cu'], 5),
    '_triggers5': test_o_random(matrices['_cl'], 5),
    '_triggers6': test_o_random(matrices['_cu'], 5),
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
