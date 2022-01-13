# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
from indicators.base import Indicator


class DownSwing(Indicator):
    """
    This will present only the down swings from the MACD.
    """
    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.

        NOTE: This ont is a little different as it uses averages that are independent of the chart 2 pix class.
        """
        self.config(options, style, **kwargs)
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
        a, b, c = self.guides  # Line, small, big.
        name = '_down_swing_' + self.source + '_' + str(a) + '_' + str(b) + '_' + str(c)
        averages = gp.macd(source, self.guides)
        line = averages[0][1]  # Use the second as the first is an X coord.
        averages[:, 1::2] = np.subtract(averages[:, 1::2], line)  # Transform center point to zero.
        averages[:, 0::2] += 6  # TODO: This is going to need to be the offset.
        solution = list()
        for idx, point in enumerate(averages[2]):  # Gather points lower than the line.
            if not np.mod(idx, 2):
                solution.append(point)
            else:
                tap = 0
                if point > tap:
                    tap = point
                solution.append(tap)
        solution[1::2] = np.multiply(solution[1::2], -1)
        self.solution = np.array(solution)
        self.style['main'][name] = self.solution
        self.style['main'][name + '_trig'] = np.array(self.solution[1::2])
        self.collect(pmatrix, fmatrix)
        return self


indicator = DownSwing
