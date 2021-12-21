# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This a graph on feed-hit variety and won't work unless chart_variety is enabled in settings.
"""

from indicators.base import Indicator


class Variety(Indicator):
    """
    This is hit-variety tracked by moving average.
    """
    variety_data = None

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.

        """
        self.config(options, style, **kwargs)
        self.variety_data = self.style['main']['_variety']
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        self.source = 'feed'
        source = fmatrix
        name = self.source + '_variety_' + str(self.ema_spread)
        if self.variety_data:
            self.ma = gp.convert_to_pixels(source, self.variety_data, relative_transform=True)
            if self.ema_spread:
                self.ma = gp.ema(
                    source,
                    self.ma,
                    # Convert to pixels so the scaling is accurate.
                    self.ema_spread,
                    prefix='variety'
                )
        else:
            self.ma = [0] * len(source.center_averages)
        self.style['main'][name] = self.ma
        self.solution = self.ma
        return self


indicator = Variety
