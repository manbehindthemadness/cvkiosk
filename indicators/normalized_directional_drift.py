# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted ema normalized.
"""

from indicators.base import Indicator
from indicators.pure_normal import PureNormal
norm = PureNormal()


class ENO(Indicator):
    """
    This is feed adjusted ema normalized.
    """
    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        mas = self.options['popt']['mas']
        if self.ema_spread is None:
            raise ValueError
        if self.ema_spread not in mas:
            mas.append(self.ema_spread)
        self.options['popt'].update({'mas': mas})
        self.options['fopt'].update({'mas': mas})
        kwargs.update({'source': 'feed'})
        norm.configure(self.options, self.style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        pmatrix, fmatrix = args
        gp = self.gp
        np = self.np
        source = pmatrix
        if self.source == 'feed':
            source = fmatrix
        name = '_eno_' + self.source + '_' + str(self.normal_base) + '_' + str(self.normal_spread) + '_' \
               + str(self.ema_spread) + '_' + self.polarity
        if name not in self.style['main'].keys():
            norm.solve(*args)
            self.normal = norm.solution
            floating_average = gp.directional_drift(
                source,
                self.polarity,
                self.ema_spread,
                self.normal
            )
            normalized_average_ys = gp.moving_average(source, floating_average[1::2], 2, prefix='eno_')
            normalized_average_ys = np.multiply(normalized_average_ys, -500)
            normalized_average_xs = floating_average[0::2][-len(normalized_average_ys):]
            normalized_average = np.array([0] * (len(normalized_average_ys) * 2))
            normalized_average[0::2] = normalized_average_xs
            normalized_average[1::2] = normalized_average_ys
            self.solution = normalized_average
            self.style['main'][name] = self.solution
        else:
            self.solution = self.style['main'][name]
        self.collect(pmatrix, fmatrix)
        return self


indicator = ENO
