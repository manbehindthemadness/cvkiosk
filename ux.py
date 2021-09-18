# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import numpy as np
import tkinter as tk
import graphiend as gp
from api import GetChart
from utils import (
    config,
    style_parser,
    constants_parser,
    layout_parser,
    matrix_parser,
    matrix_sorter,
    test_o_random,
)
from uxutils import setup


class OnScreen:
    """
    This will configure, refresh and draw our user interface.
    """
    base = None
    ticker = None
    header = None
    layout = None
    style = None
    constants = None
    matrices = dict()
    price_matrix = None
    feed_matrix = None
    price_chart = None
    feed_chart = None
    alerts = None
    chart_data = None
    matrix_solver = None

    timeframes = {
        '15minute': '15M',
        '30minute': '30M',
        '1hour': '1H',
        '4hour': '4H',
        '1day': '1D'
    }

    def __init__(self):
        self.parent = tk.Tk()
        self.cache = gp.ImgCache().refresh()  # Init the cache.
        self.settings = config('settings')  # Grab our settings.
        self.api = GetChart()

        setup(self.settings)  # Prep environment for display.

    def refresh_api(self):
        """
        This will refresh the imformation from the api.
        """
        cd = self.chart_data = self.api.get_chart()
        self.alerts, self.price_chart, self.feed_chart = cd.alerts, cd.chart, cd.feed
        return self

    def solve_matrices(self, matrix: [list, np.array], prefix: str = None) -> np.array:
        """
        This will convert price data into sweet sweet pixels.
        """
        focus = self.settings['chart_focus']
        if not focus:
            focus = 'BTC'
        pair = self.settings['chart_pair']
        ctime = self.settings['chart_time']
        timequote = self.timeframes[ctime] + ':' + focus + '/' + pair

        s = self.style
        mat = gp.ChartToPix(self.layout, *self.style['main']['price_matrix_offsets'])
        mat.solve(
            price_data=matrix,
            increment=s['main']['price_increment'],
            timequote=timequote
        )
        matrix_sorter(
            mat,
            self.matrices,
            prefix
        )
        if self.settings['style'] == 'tutorial':  # This is for the example setup only.
            self.matrices.update({
                '_triggers1': test_o_random(self.matrices['_cu'], 5),
                '_triggers2': test_o_random(self.matrices['_cl'], 5),
                '_triggers3': test_o_random(self.matrices['_ac'], 5),
                '_triggers4': test_o_random(self.matrices['_cu'], 5),
                '_triggers5': test_o_random(self.matrices['_cl'], 5),
                '_triggers6': test_o_random(self.matrices['_cu'], 5),
            })
        return mat

    def update_style_matrices(self):
        """
        This updates the price and volume matrices in our style so it can bbe passed to the widgets.
        """
        self.style = matrix_parser(self.style, self.matrices)
        return self

    def parse(self):
        """
        This will take all the configurable variables and parse their variables.
        """
        self.refresh_api()  # Get data from servers.
        layout_uninit = layout_parser(  # Get layout widgets.
            self.settings['layout']
        )
        self.constants = constants_parser(  # Get screen and geometry constants.
            self.settings['constants'],
        )
        self.style = style_parser(  # Get style sheet.
            'tutorial',
            self.constants
        )
        mstyle = self.style['main']
        mstyle['_alerts'] = gp.samples.alerts['alert_data']  # Pull sample alert data for the ticker tape.
        self.parent.geometry = mstyle['geometry']  # Configure the UX size.

        self.base = tk.Frame(
            self.parent,
            width=self.constants['_screen_width'],
            height=self.constants['_screen_height'],
            bg=mstyle['background'],
            bd=0,
            highlightthickness=0
        )
        self.base.pack(expand=True, fill='both')

        self.layout = layout_uninit(self.base, self.cache, self.settings)  # Init the layout.
        self.layout.configure(
            bg=mstyle['background'],
            width=mstyle['price_canvas_width'],
            height=mstyle['price_canvas_height'],
            bd=0,
            highlightthickness=0
        )  # Configure the price chart size.
        self.price_matrix = self.solve_matrices(self.price_chart)
        self.feed_matrix = self.solve_matrices(self.feed_chart, 'feed')
        self.update_style_matrices()  # Add the values into the style.

        if 'ticker' in self.style.keys():
            t = self.style['ticker']['style']
            self.ticker = self.layout.ticker
            self.ticker.configure(
                width=self.constants['_screen_width'],
                height=self.constants['_screen_height'],
                bg=t['background']
            )
            self.ticker.place(
                x=t['x'],
                y=t['y']
            )

    def configure(self):
        """
        This will configure the widgets with our new style information.
        """
        self.layout.configure_widgets(self.style)
        return self

    def draw(self):
        """
        This will draw our widgets against the parent user interface.
        """
        # TODO: We need to figure out how we are going to clear the data and such for update here.
        self.layout.draw_widgets()
        return self

    def mainloop(self):
        """
        runs out UX mainloop.
        """
        self.parent.mainloop()
        return self

    def run(self):
        """
        Experimental runtime setup.
        """
        self.parse()
        self.configure()
        self.draw()
        self.mainloop()
