# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted exponential moving average.
"""

from indicators.base import Indicator
from indicators.normal import Normal
norm = Normal()


class FAEMA(Indicator):
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
        mas = self.options['popt']['mas']
        if self.ema_spread not in mas:
            mas.append(self.ema_spread)
        self.options['popt'].update({'mas': mas})
        kwargs.update({'source': 'feed'})
        norm.configure(self.options, self.style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        name = '_faema_' + str(self.normal_base) + '_' + str(self.normal_spread) + '_' + str(self.ema_spread)
        if name not in self.style['main'].keys():
            norm.solve(*args)
            self.normal = norm.solution
            cross = gp.convert_to_pixels(pmatrix, pmatrix.center_averages)  # Convert to pixels so the scaling is accurate.
            solution = gp.cross_normalize(
                pmatrix,
                self.normal,
                cross,
                self.ema_spread,
                prefix='cross_'
            )
            self.style['main'][name] = solution
        else:
            solution = self.style['main'][name]
        self.collect(pmatrix, fmatrix)
        self.solution = solution
        # NOTE: We aren't going to trim this to the view range as we will be using it to attach other trends elsewhere.
        return self


indicator = FAEMA
