# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This file is where we store various price and chart post processing utilities,
    think of it as a pluggable math playground.
"""

import numpy as np
import graphiend as gp


NoneType = type(None)  # https://stackoverflow.com/questions/40553285/determining-a-variables-type-is-nonetype-in-python/40553322


class Filters:
    """
    This will basically house various methods that will produce some change to the passed matrix data.
    """
    matrix = None
    vrange = None

    def __init__(self, style: dict):
        self.style = style
        self.mstyle = self.style['main']

    def inkeys(self, name: str) -> [bool, np.array]:
        """
        This just checks to see if a value has already been calculated.
            If yes it will return the value from the style.
            Tf no it will return None.
        """
        result = None
        if name in self.mstyle.keys():
            result = self.mstyle[name]
        return result

    def configure(self, matrix: gp.ChartToPix):
        """
        This just sets up a bunch of variables.
        """
        self.matrix = matrix
        self.vrange = np.multiply(matrix.viewable_increment_count, 2)
        return self

    def trim(self, ary: np.array) -> np.array:
        """
        This trims our output to the viewable range and scales it to the proper size.

        NOTE: This needs to be performed on the raw adjusted array once!
        """
        trm = np.array(ary[-self.vrange:])
        vmax = np.amax(trm[1::2])
        vmin = np.amin(trm[1::2])
        height = np.subtract(vmax, vmin)
        ary[1::2] = gp.scale(ary[1::2], height, self.matrix.viewable_increment_count)
        return np.array(ary)

    def ema(self, points: np.array, spread: int = 20, ) -> np.array:
        """
        You guessed it, and exponencial moving average.
        """
        name = '_ema_' + str(spread)
        average = self.inkeys(name)
        if isinstance(average, NoneType):
            # average = self.trim(points)
            average = points
            average = gp.smooth_y(np.array(average), spread)
            self.mstyle[name] = average
        return np.array(average)

    def normalize(self, points: np.array, base_spread: int, spread: int) -> np.array:
        """
        This will normalize a series of measurements by taking two averages and subtracting the base_spread ema
            from the spread ema.
        """
        name = '_normal_' + str(base_spread) + '_' + str(spread)
        normal = self.inkeys(name)
        if isinstance(normal, NoneType):
            ema = self.ema(points, base_spread)
            normal = self.ema(points, spread)
            normal[1::2] = np.subtract(normal[1::2], ema[1::2])
            self.mstyle[name] = normal
        return np.array(normal)
