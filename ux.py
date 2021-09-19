# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import random
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
    base_style = None
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
    delay = None
    meter_vars = list()
    labels = list()
    meter_text = None

    timeframes = {
        '15minute': '15M',
        '30minute': '30M',
        '1hour': '1H',
        '4hour': '4H',
        '1day': '1D'
    }

    def __init__(self, debug_mode: bool = False):
        self.parent = tk.Tk()
        self.cache = gp.ImgCache().refresh()  # Init the cache.
        self.settings = config('settings')  # Grab our settings.
        self.api = GetChart()
        self.debug_mode = debug_mode

        setup(self.settings)  # Prep environment for display.

    def refresh_api(self):
        """
        This will refresh the imformation from the api.
        """
        if not self.debug_mode:
            self.chart_data = self.api.get_chart()
            cd = self.chart_data
            self.alerts, self.price_chart, self.feed_chart = cd.alerts, cd.chart, cd.feed
        else:
            data = gp.samples.price_data
            random.shuffle(data)
            self.price_chart = list(data)
            random.shuffle(data)
            self.feed_chart = list(data)
            self.alerts = gp.samples.alerts
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
        mat = gp.ChartToPix(self.layout, *self.style['main']['price_matrix_offsets'], w_h=(
            s['main']['price_canvas_width'],
            s['main']['price_canvas_height']
        ))
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
        return mat

    def update_style_matrices(self):
        """
        This updates the price and volume matrices in our style so it can bbe passed to the widgets.
        """
        self.style['main']['_alerts'] = self.alerts  # Pull sample alert data for the ticker tape.
        self.matrices = dict()
        self.price_matrix = self.solve_matrices(self.price_chart)
        self.feed_matrix = self.solve_matrices(self.feed_chart, 'feed')
        if self.settings['style'] == 'tutorial':  # This is for the example setup only.
            print('drawing example randoms')
            self.matrices.update({
                '_triggers1': test_o_random(self.matrices['_cu'], 5),
                '_triggers2': test_o_random(self.matrices['_cl'], 5),
                '_triggers3': test_o_random(self.matrices['_ac'], 5),
                '_triggers4': test_o_random(self.matrices['_cu'], 5),
                '_triggers5': test_o_random(self.matrices['_cl'], 5),
                '_triggers6': test_o_random(self.matrices['_cu'], 5),
            })
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

        # Get the values for the stat bar.

        self.meter_vars = list()
        self.labels = list()  # minus the left and right stat meter.
        extras = np.add(self.constants['_extra_labels'], 2)  # Add 2 to account for the battery ans wifi meters.
        if extras > 10:
            raise ValueError
        for idx in range(0, extras):
            if idx < 2:
                self.meter_vars.append(tk.IntVar())
            else:
                self.meter_vars.append(tk.StringVar())
            self.labels.append(tk.Label())

        self.meter_text = [
            'BAT',
            'WFI',
            'fgi',
            'quo',
            'ext',
            'ext',
            'ext',
            'ext',
            'ext',
            'ext',
        ]
        # TODO: Remove after testing.
        self.meter_vars[0].set(75)
        self.meter_vars[1].set(75)
        for tvar, txt in zip(self.meter_vars[2:], self.meter_text[2:]):
            tvar.set(txt)

        self.constants.update({
            '_labels': self.labels,
            '_stat_variables': self.meter_vars,
            '_stat_text': self.meter_text,
        })

        self.style = style_parser(  # Get style sheet.
            'tutorial',  # TODO: THis has to come from config.
            self.constants
        )

        mstyle = self.style['main']
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

        self.base_style = dict(self.style)
        self.update_style_matrices()  # Add the values into the style.

        if 'ticker' in self.style.keys() and not self.ticker:
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
        return self

    def configure(self):
        """
        This will configure the widgets with our new style information.
        """
        self.layout.configure_widgets(self.style)
        self.layout.configure_actors()
        return self

    def draw(self):
        """
        This will draw our widgets against the parent user interface.
        """
        self.layout.draw_widgets()
        return self

    def mainloop(self):
        """
        runs out UX mainloop.
        """
        self.parent.mainloop()
        return self

    def purge(self, prep: bool = False):
        """
        Removes all our variables in order to redraw.
        """
        if prep:  # TODO: This will need to be evaluated to maximize our redraw speeds.
            self.price_chart = None
            self.feed_matrix = None
            self.price_matrix = None
            self.feed_chart = None
            self.alerts = None
            self.chart_data = None
            self.matrix_solver = None
            self.style = dict(self.base_style)
            self.layout.purge()
        else:
            self.layout.delete('all')
        return self

    def refresh(self):
        """
        This will refresh our chart data.
        """
        self.purge(prep=True)
        self.refresh_api()  # Launching this here will fire off the api twice really fast.... need to fix this.
        self.update_style_matrices()
        self.configure()
        self.purge()
        self.draw()  # Test to see if we are properly clearing the images.

    def cycle(self):
        """
        This will loop our refresh cycle.
        """
        if not self.delay:
            self.delay = int(np.multiply(np.multiply(self.settings['update_time'], 60), 1000))
        self.refresh()
        print('refreshing!', self.style['main']['_price_quote'])
        self.parent.after(self.delay, self.cycle)

    def run(self):
        """
        Experimental runtime setup.
        """
        self.parse()
        self.cycle()
        self.layout.configure_actors()
        self.layout.animate_actors()
        self.mainloop()
