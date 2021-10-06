# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This file is where we store various price and chart post processing utilities,
    think of it as a pluggable math playground.

TODO: Even though this is all kinds of fun we are going to eventually have to transfer these calculations
    to source the original feed data in order to remain accurate when it comes to smaller screens.

    SOMETHING IN HERE IS FUCKED
"""

import numpy as np
import graphiend as gp
from utils import flip_stream


NoneType = type(None)  # https://stackoverflow.com/questions/40553285/determining-a-variables-type-is-nonetype-in-python/40553322


class Filters:
    """
    This will basically house various methods that will produce some change to the passed matrix data.
    """
    matrix = None
    vrange = None
    polarity = None

    def __init__(self):
        self.style = None

    def inkeys(self, name: str) -> [bool, np.array]:
        """
        This just checks to see if a value has already been calculated.
            If yes it will return the value from the style.
            Tf no it will return None.

            TODO: THIS IS THE SOURCE OF OUR UPDATE PROBLEM.
                    This also indicates that the style main section isn't getting updated.
        """
        result = None
        if name in self.style['main'].keys():
            result = self.style['main'][name]
        return result

    def configure(self, style: dict, matrix: gp.ChartToPix):
        """
        This just sets up a bunch of variables.
        """
        self.clear()
        self.style = style
        self.matrix = matrix
        self.vrange = np.add(np.multiply(matrix.viewable_increment_count, 2), 2)
        return self

    def clear(self):
        """
        This purges our variables.
        """
        self.style = None
        self.matrix = None
        self.vrange = None

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
        return ary

    def ema(self, points: np.array, spread: int = 20, ) -> np.array:
        """
        You guessed it, and moving average.
        """
        name = '_ema_' + str(spread)
        average = flip_stream(points)
        ays = gp.moving_average(np.array(average[1::2]), spread)
        padding = np.subtract(spread, 1)
        average[1::2] = np.pad(ays, (padding, 0))
        self.style['main'][name] = np.array(average)
        return np.array(average)

    def normalize(self, points: np.array, base_spread: int, spread: int) -> np.array:
        """
        This will normalize a series of measurements by taking two averages and subtracting the base_spread ema
            from the spread ema.
        """
        name = '_normal_' + str(base_spread) + '_' + str(spread)
        ema = self.ema(points, base_spread)
        normal = self.ema(points, spread)
        normal[1::2] = np.subtract(normal[1::2], ema[1::2])
        self.style['main'][name] = np.array(normal)
        return normal

    def cross_normalize(self, normal: np.array, points: np.array, spread: int = 26, offset: int = 0) -> np.array:
        """
        This will take a normalized price plot and conform it to a secondary set of coordinates.

        TODO: I don't think using offset is going to work as the screens layouts vary...
        """
        _ema = self.ema(points, spread)
        cross = np.array(normal)
        cross[1::2] = np.add(np.add(_ema[1::2], offset), cross[1::2])
        name = '_cross_normal_' + str(spread)
        self.style['main'][name] = np.array(cross)
        return cross

    def find_polarity(self, points: np.array):
        """
        Merely discovers if we are moving isn a positive or negitive direction.
        """
        self.polarity = list()
        for idx, point in enumerate(points):
            if not idx:  # Skip the first iteration.
                pass
            else:
                ls = np.subtract(idx, 1)
                last = np.abs(points[ls])
                this = np.abs(point)
                polarity = 1
                if last > this:
                    polarity = 0
                self.polarity.append(polarity)
        return self

    def trender(self, points: np.array, prefix: str = '') -> np.array:
        """
        This identifies the trend cycle direction of the supplied points.
        """
        if prefix:
            prefix = '_' + prefix
        ys = [0]
        points = np.array(points)
        pts = points[1::2]
        for idx, point in enumerate(pts):
            if not idx:
                pass
            else:
                ls = np.subtract(idx, 1)
                last = pts[ls]
                pt = 0
                if last < point:
                    pt = 1
                ys.append(pt)
        name = prefix + '_trend'
        self.style['main'][name] = np.array(ys)
        name = prefix + '_anti_trend'
        ys = np.add(np.multiply(ys, -1), 1)
        self.style['main'][name] = np.array(ys)
        return ys

    def drifter(self, points: np.array, prefix: str = '') -> np.array:
        """
        This is much like trender, except it's for graphing instead of an alert trigger.
        """
        if prefix:
            prefix = '_' + prefix
        result = np.linspace(0, 0, num=len(points)).astype(np.int)
        result[0::2] = np.array(points[0::2])
        ys = np.array(points[1::2])
        yts = [0]
        for idx, point in enumerate(ys):
            if not idx:
                pass
            else:
                last = ys[np.subtract(idx, 1)]
                this = point
                drift = np.subtract(this, last)
                yp = 0
                if drift > -1:
                    yp = this
                yts.append(yp)
        result[1::2] = np.multiply(yts, -1)
        name = prefix + '_drift'
        self.style['main'][name] = np.array(result)
        trend = list()
        for point in np.array(result[1::2]):
            pt = 0
            if point != 0:
                pt = 1
            trend.append(pt)
        name = prefix + '_trend'
        self.style['main'][name] = np.array(trend)
        return result

    def oscillator(self, points: np.array) -> np.array:
        """
        This will identify the points of trend shifts from negative and positive.

        This expects the output of trender.
        """
        utrends = [0]
        dtrends = [0]
        pts = np.array(points)
        for idx, point in enumerate(pts):
            if idx < 1:
                pass
            else:
                chk = 7
                if idx < 7:
                    chk = idx
                start, end, check = np.subtract(idx, 1), np.add(idx, 4), np.subtract(idx, chk)

                holder = pts[start: idx]
                teller = pts[idx: end]
                ut = dt = 0
                if 0 not in holder and pts[idx] == 0 and 1 not in teller:  # This here is just a fancy filter.
                    seer = utrends[check: idx]
                    if 1 not in seer and len(teller) == 4:
                        utrends[np.subtract(idx, 4)] = 1
                elif 1 not in holder and pts[idx] == 1 and 0 not in teller:
                    seer = dtrends[check: idx]
                    if 1 not in seer and len(teller) == 4:
                        dtrends[np.subtract(idx, 4)] = 1
                utrends.append(ut)
                dtrends.append(dt)
        name = '_utrends'
        self.style['main'][name] = np.array(utrends)
        name = '_dtrends'
        self.style['main'][name] = np.array(dtrends)
        return [utrends, dtrends]
