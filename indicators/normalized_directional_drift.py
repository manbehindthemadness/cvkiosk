# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted ema normalized.
"""

from indicators.base import Indicator


class ENO(Indicator):
    """
    This is feed adjusted ema normalized.
    """
    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
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
        name = '_eno_' + self.source
        if name not in self.style['main'].keys():

            floating_average = gp.drifter(source)

            self.solution = floating_average
            self.style['main'][name] = self.solution
        else:
            self.solution = self.style['main'][name]
        self.collect(pmatrix, fmatrix)
        return self


indicator = ENO
