# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This normalized moving average.
"""

from indicators.base import Indicator


class Normal(Indicator):
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
        self.options['popt'].update({'mas': mas})
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
        normal_name = '_normal_' + str(self.normal_base) + '_' + str(self.normal_spread)
        if normal_name not in self.style['main'].keys():  # Ensure we don't re-calculate something we already have.
            self.normal = gp.normalize(
                source,
                # source.price_matrix[-1],
                gp.convert_to_pixels(source, source.center_averages),  # Convert to pixels so the scaling is accurate.
                self.normal_base,
                self.normal_spread,
                prefix=''
            )
            self.style['main'][normal_name] = self.normal
        else:
            self.normal = self.style['main'][normal_name]
        solution = self.normal
        self.collect(pmatrix, fmatrix)
        self.solution = solution
        # NOTE: We aren't going to trim this to the view range as we will be using it to attach other trends elsewhere.
        return self


indicator = Normal
