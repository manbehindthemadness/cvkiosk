# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted on balance volume.
"""

from indicators.base import Indicator
from indicators.on_balance_volume import OBV


class FAOBV(Indicator):
    """
    See docstring.
    """

    def __init__(self):
        Indicator.__init__(self)
        self.obv = OBV()

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        kwargs.update({'source': 'price'})
        self.obv.configure(options, style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.

        Remember here we don't actually need to normalize because the obv is already attached to the closing price.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        self.obv.solve(*args)
        obv = self.obv.solution
        self.normal = gp.moving_average(
            pmatrix,
            obv,
            self.obv_spread,
            prefix='_obv_'
        )
        name = '_faobv_' + str(self.normal_base) + '_' + str(self.normal_spread) + '_' + str(self.obv_spread)
        # if name not in self.style['main'].keys():
        #     self.obv.solve(*args)
        #     obv = self.obv.solution
        #     normal = gp.normalize(
        #         pmatrix,
        #         obv,
        #         self.normal_base,
        #         self.normal_spread,
        #         prefix='_obv_price_'
        #     )
        #     faema, obv = gp.un_jag([
        #         faema, obv
        #     ])
        #     solution = gp.cross_normalize(
        #         pmatrix,
        #         obv,
        #         faema,
        #         prefix='_obv_cross'
        #     )
        #     self.style['main'][name] = solution
        # else:
        #     solution = self.style['main'][name]
        # self.collect(pmatrix, fmatrix)
        # self.solution = solution
        # return self
        self.solution = self.normal
        self.style['main'][name] = self.solution
        return self


indicator = FAOBV
