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
import copy
import threading
import datetime
import gc
import random
import linecache
import numpy as np
import tkinter as tk
import graphiend as gp
from pathlib import Path
from api import GetChart
from utils import (
    log,
    config,
    style_parser,
    constants_parser,
    layout_parser,
    matrix_parser,
    matrix_sorter,
    get_index,
)
from indicators.base import Dummy
from uxutils import ScrCap
from rpi import wifi_sig
if config('settings')['debug_memory']:
    from diagnostics import MemTrace

from sugar import Sugar


cap_file = Path('www/chart.png')
screen_cap = ScrCap(cap_file)


class OnScreen(tk.Tk):
    """
    This will configure, refresh and draw our user interface.
    """
    runner = 0

    init = True

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
    variety = None
    alerts = None
    chart_data = None
    matrix_solver = None
    delay = None

    indicators = list()
    delayed_indicators = ['audio_alerts']  # These indicators need to be processed after the rest have been solved.
    indicator_alerts = list()

    sugar = None

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

    def __init__(self):
        tk.Tk.__init__(self)
        self.cache = gp.ImgCache().refresh()  # Init the cache.
        self.settings = config('settings')  # Grab our settings.
        self.api = GetChart()
        self.debug_mode = self.settings['debug_data']
        self.filters = None
        self.faker = None

        try:
            self.sugar = Sugar()
            self.sugar.battery_gpio_set()
        except (NameError, FileNotFoundError):
            pass

        if self.settings['debug_memory']:
            self.trace = MemTrace()  # Fire up a tracer and watch for leaks.

        self.config(cursor="none")

    def refresh_api(self):
        """
        This will refresh the imformation from the api.
        """
        try:
            self.chart_data = self.api.get_chart()
        except TypeError as err:
            log('Unable to acquire chart data, please check the API key and connection string', err, '*crit*')
            exit()
        cd = self.chart_data
        if self.debug_mode:
            random.shuffle(cd.chart)
            random.shuffle(cd.feed)
        self.variety, self.alerts, self.price_chart, self.feed_chart = cd.variety, cd.alerts, cd.chart, cd.feed
        return self

    def solve_matrices(self, matrix: [list, np.array], options: dict, prefix: str = '') -> np.array:
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
        options = options
        mat.solve(
            price_data=matrix,
            increment=s['main']['price_increment'],
            timequote=timequote,
            **options
        )
        matrix_sorter(
            mat,
            self.matrices,
            prefix
        )
        if prefix:
            prefix += '_'
        self.style[prefix + 'extras'] = mat.extras
        return mat

    def process_indicators(self) -> dict:
        """
        This will import and process the various indicators that are specified in our style.
        """
        indicator = Dummy

        opts = indicator().options
        idrs = self.style['indicators']
        if not self.indicators:
            for idr in idrs:
                if idr not in self.delayed_indicators:
                    cmd = 'from indicators.' + idr + ' import indicator as ' + idr
                    exec(cmd)
                    indicator = eval(idr)
                    for kw in self.style['indicators'][idr]:
                        i = indicator().configure(opts, self.style, **kw)
                        opts = i.options
                        self.indicators.append(i)
        else:
            slip = 0
            for idr in idrs:
                if idr not in self.delayed_indicators:
                    for kw in self.style['indicators'][idr]:
                        i = self.indicators[slip]
                        i.configure(opts, self.style, **kw)
                        opts = i.options
                        slip += 1
        return opts

    def solve_indicators(self):
        """
        This will go though and trigger the math processes to add our indicator coordinated into the main style.
        """
        self.style['main']['_ac'] = self.price_matrix.price_matrix[-1]  # pull this early in the event we need it for an indicator.
        for indicator in self.indicators:
            indicator.solve(self.price_matrix, self.feed_matrix)
        return self

    def solve_delayed_indicators(self):
        """
        This will process the delayed indicators.
        """
        alert = Dummy

        opts = alert().options
        idrs = self.style['indicators']
        if not self.indicator_alerts:
            for idr in idrs:
                if idr in self.delayed_indicators:
                    cmd = 'from indicators.' + idr + ' import indicator as ' + idr
                    exec(cmd)
                    alert = eval(idr)
                    for kw in self.style['indicators'][idr]:
                        i = alert().configure(opts, self.style, **kw)
                        self.indicator_alerts.append(i)
        else:
            slip = 0
            for idr in idrs:
                if idr in self.delayed_indicators:
                    for kw in self.style['indicators'][idr]:
                        i = self.indicator_alerts[slip]
                        i.configure(opts, self.style, **kw)
                        slip += 1
        for alert in self.indicator_alerts:
            alert.solve()
        return self

    def update_style_matrices(self):
        """
        This updates the price and volume matrices in our style so it can bbe passed to the widgets.

        """
        self.style['main']['_alerts'] = self.alerts  # Pull sample alert data for the ticker tape.
        self.style['main']['_variety'] = self.variety
        self.matrices = dict()
        options = self.process_indicators()
        self.price_matrix = self.solve_matrices(self.price_chart, options['popt'])
        self.feed_matrix = self.solve_matrices(self.feed_chart, options['fopt'], 'feed')
        self.style['main']['_drf'] = [str(np.round(float(self.feed_chart[-1][-1]), 3))]
        self.solve_indicators()
        self.style = matrix_parser(self.style, self.matrices)  # Explode coordinates into style.
        self.solve_delayed_indicators()
        return self

    def screen_cap(self, coords: tuple, enhance: bool = False):
        """
        This will take the screenshot we will host with our cute little dash server.
        NOTE: This will only capture the graphiend chart region ( not stats and tickers )
        """

        screen_cap.capture(coords)
        if enhance:
            screen_cap.enhance()
        return self

    def hide_faker(self):
        """
        This hides the screen faker deal.
        """
        self.faker.hide()
        self.after(1000, self._screen_cap)

    def _screen_cap(self):
        """
        This is a threaded wrapper for screen_cap
        """
        ox, oy = self.settings['capture_offsets']
        x1 = np.add(self.layout.winfo_x(), ox)
        y1 = np.add(self.layout.winfo_y(), oy)
        x2 = np.add(x1, self.layout.winfo_width())
        y2 = np.add(y1, self.layout.winfo_height())
        coords = (x1, y1, x2, y2,)
        th = threading.Thread(target=self.screen_cap, args=(coords, False))
        th.start()
        th.join()
        return self

    def read_hardware(self):
        """
        This will get variables from the system hardware
        """
        bat_lvl = -1
        try:
            if self.sugar:
                self.sugar.capacity()
                bat_lvl = self.sugar.BATTERY_LEVEL
            self.statvars['BAT'] = bat_lvl
        except OSError:
            pass
        return self

    def update_statbar_variables(self):
        """
        This is where we will iterate through the layout.labelvars dict and pass the stat-bar variables.
        We can loop this method in an alternate thread for faster updates.

        NOTE: These are for the stat-bar only.
        """
        if not self.settings['headless']:
            self.read_hardware()
            try:
                asset = self.settings['chart_focus'].upper()
                if not asset:
                    asset = 'BTC'
                asset += ' / ' + self.settings['chart_pair'].upper()
                self.statvars['TIK'] = asset
                self.statvars['WFI'] = wifi_sig()
                self.statvars['UTC'] = datetime.datetime.utcnow().strftime(self.style['main']['utc_format'])  # noqa
                self.statvars['DRF'] = np.round(float(self.feed_chart[-1][-1]), 3)
                self.statvars['QUO'] = np.round(float(self.price_chart[-1][-2]), 3)  # TODO: Need to figure out how we handle small values.
                for var in self.statvars:
                    if var in self.layout.labelvars.keys() and var not in ['WFI', 'BAT']:
                        rnd = var + ': ' + str(self.statvars[var])  # noqa
                        exec('self.layout.statbar.' + var + '.set(rnd)')
                    elif var in self.layout.labelvars.keys() and var in ['WFI', 'BAT']:
                        self.layout.labelvars[var].set(self.statvars[var])
                self.layout.statbar.refresh()
            except (AttributeError, TypeError) as err:
                print('failed to populate variables')
                print(err)
                pass
        return self

    def cycle_index(self):
        """
        This is a temporary refresh loop for the fear and greed index.
        """
        if 'FGI' in self.layout.labelvars.keys():
            index = get_index()
            self.statvars['FGI'] = index
        self.after(1800000, self.cycle_index)
        return self

    def cycle_variables(self):
        """
        This is the statbar refresh loop.
        """
        self.update_statbar_variables()
        self.after(self.settings['stats_refresh'], self.cycle_variables)
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
        self.geometry = mstyle['geometry']  # Configure the UX size.

        # This here is going to hold a screenshot that we are going to use to hide the redraw process.
        # TODO: This sounded like a good idea but the application hangs whenever I try to open the file -_-
        self.base = tk.Frame(
            self,
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

        self.base_style = copy.deepcopy(self.style)  # Turns out this is the only way to handle nested dicts.
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
        from widgets import Faker
        self.faker = Faker(self, self.layout)
        return self

    def configure_layout(self):
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

    def purge(self, prep: bool = False):
        """
        Removes all our variables in order to redraw.
        https://stackoverflow.com/questions/57462037/what-are-count0-count1-and-count2-values-returned-by-the-python-gc-get-count
        """
        if prep:  # TODO: This will need to be evaluated to maximize our redraw speeds.
            self.matrices = None
            self.price_chart = None
            self.feed_matrix = None
            self.price_matrix = None
            self.feed_chart = None
            self.alerts = None
            self.chart_data = None
            self.matrix_solver = None
            self.style = copy.deepcopy(self.base_style)  # Turns out this is the only way to handle nested dicts.
            self.layout.purge()
        else:
            self.layout.delete('all')
        return self

    def refresh(self):
        """
        This will refresh our chart data.
        """
        print('refreshing data')
        if not self.init and not self.settings['headless']:
            print('waiting on foreign lock')
            self.wait_variable(self.layout.ticker.foreign_lock)
            print('setting initial ticker')
            self.layout.ticker.initial = True  # This prevents the extra delay cycle.
        print('showing faker')
        self.faker.show()
        print('purging memory with prep')
        self.purge(prep=True)
        print('refreshing api')
        self.refresh_api()  # Launching this here will fire off the api twice really fast.... need to fix this.
        print('updating style matrices')
        self.update_style_matrices()
        print('configuring layout')
        self.configure_layout()
        print('purging memory')
        self.purge()
        print('handling memory usage')
        self.handle_memory()
        print('drawing interface')
        self.draw()  # Test to see if we are properly clearing the images.
        print('updating stat bar variables')
        self.update_statbar_variables()
        print('waiting on capture')
        self.after(self.settings['capture_delay'], self.hide_faker)
        print('refreshing cache')
        self.cache.refresh(resave=True)
        return self

    def cycle(self):
        """
        This will loop our refresh cycle.
        """
        if not self.delay:
            self.delay = int(np.multiply(np.multiply(self.settings['update_time'], 60), 1000))
        self.refresh()
        self.after(self.delay, self.cycle)

        return self

    def run(self):
        """
        Experimental runtime setup.
        """
        self.parse()  # Remember we only parse once, so persistent variables need to be updated per-run.
        self.cycle()
        self.cycle_index()
        self.layout.configure_actors()
        self.layout.animate_actors()
        self.cycle_variables()
        self.init = False
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
