# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is normalized moving average.
"""

from indicators.base import Indicator


class MA(Indicator):
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
        suffix = str()
        if self.suffix:
            suffix = self.suffix
        ma_name = self.source + '_ema_' + str(self.ema_spread) + suffix
        if ma_name not in self.style['main'].keys():  # Ensure we don't re-calculate something we already have.
            self.ma = gp.ema(
                source,
                gp.convert_to_pixels(source, source.center_averages, relative_transform=True),  # Convert to pixels so the scaling is accurate.
                self.ema_spread,
                prefix=''
            )
            self.style['main'][ma_name] = self.ma
        else:
            self.ma = self.style['main'][ma_name]
        self.collect(pmatrix, fmatrix)
        self.solution = self.ma
        return self


indicator = MA
