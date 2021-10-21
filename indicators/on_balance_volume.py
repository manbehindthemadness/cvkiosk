# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is on balanced volume...yay
"""

from indicators.base import Indicator


class OBV(Indicator):
    """
    feed adjusted exponential moving average.
    """

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        self.options['popt'].update({'obv': True})
        self.options['fopt'].update({'obv': True})
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        source = pmatrix
        if self.source == 'feed':
            source = fmatrix
        name = '_' + self.source + '_obv'
        points = source.extras['obv']
        self.solution = gp.convert_to_pixels(source, points)
        self.style['main'][name] = self.solution
        self.collect(pmatrix, fmatrix)
        return self


indicator = OBV
