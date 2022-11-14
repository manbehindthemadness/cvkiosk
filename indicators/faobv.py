# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted on balance volume.
"""

from indicators.base import Indicator


class FAOBV(Indicator):
    """
    See docstring.
    """

    def __init__(self):
        Indicator.__init__(self)
        self.faobv_spread = 1

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.

        Remember here we don't actually need to normalize because the obv is already attached to the closing price.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        name = '_faobv_' + str(self.normal_spread) + '_' + str(self.obv_spread)
        if name not in self.style['main'].keys():
            points = gp.moving_average(
                fmatrix,
                fmatrix.volume,
                self.normal_spread,
                prefix='faobv_normal_'
            )
            obv = gp.moving_average(
                pmatrix,
                pmatrix.extras['obv'],
                self.obv_spread,
                prefix='faobv_obv_'
            )
            solution = gp.on_balance_volume(
                closes=obv,
                volume=points
            )
            solution = gp.moving_average(
                pmatrix,
                solution,
                self.faobv_spread,
                prefix='faobv_spread_'
            )
            solution = gp.convert_to_pixels(pmatrix, solution)
            self.style['main'][name] = solution
        else:
            solution = self.style['main'][name]
        self.collect(pmatrix, fmatrix)
        self.solution = solution
        return self


indicator = FAOBV
