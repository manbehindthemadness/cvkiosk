# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
TODO: We need to go over every inch of this and confirm we are actually cleaning up our images
        https://github.com/pythonprofilers/memory_profiler

"""
import gc
import random
import linecache
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
from extras import Filters
if config('settings')['debug_memory']:
    from diagnostics import MemTrace


class OnScreen:
    """
    This will configure, refresh and draw our user interface.
    """
    runner = 0

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

    statvars = {
        'WFI': int(),
        'BAT': int(),
        'FGI': int(),
        'UTC': int(),
        'QUO': int(),
        'REF': int(),
    }

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
        self.filters = None

        setup(self.settings)  # Prep environment for display.

        if self.settings['debug_memory']:
            self.trace = MemTrace()  # Fire up a tracer and watch for leaks.

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

        NOTE: The extras options will allow us to add in custom post processing for our feed values
        """
        focus = self.settings['chart_focus']
        if not focus:
            focus = 'BTC'
        pair = self.settings['chart_pair']
        ctime = self.settings['chart_time']
        timequote = self.timeframes[ctime] + ':' + focus.upper() + '/' + pair.upper()

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
            self.matrices.update({
                '_triggers1': test_o_random(self.matrices['_cu'], 5),
                '_triggers2': test_o_random(self.matrices['_cl'], 5),
                '_triggers3': test_o_random(self.matrices['_ac'], 5),
                '_triggers4': test_o_random(self.matrices['_cu'], 5),
                '_triggers5': test_o_random(self.matrices['_cl'], 5),
                '_triggers6': test_o_random(self.matrices['_cu'], 5),
            })

        self.filters.configure(self.feed_matrix)
        self.filters.trender(self.feed_matrix.adjusted_price_points, 'super')
        self.filters.drifter(self.feed_matrix.adjusted_price_points, 'super')
        normal = self.filters.normalize(self.feed_matrix.adjusted_price_points, 100, 9)
        self.filters.zero_point(self.feed_matrix.adjusted_price_points, 1)
        trend = self.filters.trender(normal)
        self.filters.oscillator(trend)
        self.style = self.filters.style

        self.style = matrix_parser(self.style, self.matrices)
        return self

    def update_variables(self):
        """
        This is where we will iterate through the layout.labelvars dict and pass the statbar variables.
        We can loop this method in an alternate thread for faster updates.

        THIS IS SETUP FOR TESTING AND NEEDS REAL VARIABLES.
        """
        try:
            self.statvars['WFI'] = random.randint(50, 100)  # TODO: For testing only
            self.statvars['BAT'] = random.randint(50, 100)
            for var in self.statvars:
                if var in self.layout.labelvars.keys() and var not in ['WFI', 'BAT']:
                    rnd = var + ': ' + str(random.randint(50, 100))  # noqa
                    exec('self.layout.statbar.' + var + '.set(rnd)')
                elif var in self.layout.labelvars.keys() and var in ['WFI', 'BAT']:
                    self.layout.labelvars[var].set(self.statvars[var])
            self.layout.statbar.refresh()
        except AttributeError:
            pass
        return self

    def cycle_variables(self):
        """
        This is the statbar refresh loop.
        """
        self.update_variables()
        self.parent.after(self.settings['stats_refresh'], self.cycle_variables)
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

        self.style = style_parser(
            self.settings['style'],  # Get style sheet.
            self.constants  # Get style constants.
        )

        mstyle = self.style['main']
        self.parent.geometry = mstyle['geometry']  # Configure the UX size.
        self.filters = Filters(self.style)

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
        https://stackoverflow.com/questions/57462037/what-are-count0-count1-and-count2-values-returned-by-the-python-gc-get-count
        """
        if prep:  # TODO: This will need to be evaluated to maximize our redraw speeds.
            # self.price_chart = None
            # self.feed_matrix = None
            # self.price_matrix = None
            # self.feed_chart = None
            # self.alerts = None
            # self.chart_data = None
            # self.matrix_solver = None
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
        self.handle_memory()
        self.draw()  # Test to see if we are properly clearing the images.
        self.update_variables()
        return self

    def cycle(self):
        """
        This will loop our refresh cycle.
        """
        if not self.delay:
            self.delay = int(np.multiply(np.multiply(self.settings['update_time'], 60), 1000))
        self.refresh()
        self.parent.after(self.delay, self.cycle)

        return self

    def run(self):
        """
        Experimental runtime setup.
        """
        self.parse()
        self.cycle()
        self.layout.configure_actors()
        self.layout.animate_actors()
        self.cycle_variables()
        self.mainloop()
        return self

    def handle_memory(self):
        """
        This is some memory handling logic we are using to prevent memory leaks.
        """
        gc.collect()
        linecache.clearcache()  # This is experimental.
        if self.settings['debug_memory']:
            # Trace memory leak.
            if not np.mod(self.runner, 50):
                print('trace:' + str(self.runner), '------------------------------------------------------------------')
                self.trace.comp_n_show(6)
                pass
            self.runner += 1
            if not np.mod(self.runner, 10):
                print(self.runner)
