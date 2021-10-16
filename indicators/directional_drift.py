# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This a graph on directional drift, either negative or positive.
"""

from indicators.base import Indicator
from indicators.moving_average import MA
ma = MA()


class DDrift(Indicator):
    """
    Drift indicator.
    """

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        mas = self.options['popt']['mas']
        self.options['popt'].update({'mas': mas})
        ma.configure(self.options, self.style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        pmatrix, fmatrix = args
        ma.solve(*args)  # This will build our moving average.
        gp = self.gp
        source = pmatrix
        if self.source == 'feed':
            source = fmatrix
        dd_name = '_' + self.source + '_dd_' + str(self.ema_spread) + '_' + self.polarity
        if dd_name not in self.style['main'].keys():  # Ensure we don't re-calculate something we already have.
            self.dd = gp.directional_drift(
                source,
                self.polarity,
                self.ema_spread
            )
            self.style['main'][dd_name] = self.dd
            self.solution = self.dd
        else:
            self.solution = self.style['main'][dd_name]
        self.collect(pmatrix, fmatrix)
        return self


indicator = DDrift
