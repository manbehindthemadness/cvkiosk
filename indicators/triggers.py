# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is a unique indicator that need to be run LAST. This is because it requires the output of the other indicators to
    already be solved in order to work.
"""

from indicators.base import Indicator


class Triggers(Indicator):
    """
    See docstring
    """
    colors = dict()
    color_ranges = dict()
    triggers = dict()

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        return self

    def solve(self, *args):  # noqa
        """
        This will do the actual math and build our solution.
        """
        trigger_type = self.kwargs.pop('type')
        cmd = 'self.' + trigger_type + '(**self.kwargs)'
        exec(cmd)

    def adjust_length(self, base: str, target: str):
        """
        This will verify that our base and target arrays are the same length.
        """
        s = self.style['main']
        gp = self.gp
        np = self.np
        base, target = np.array(s[base]), np.array(s[target])
        base, target = gp.un_jag([base, target])
        return base, target

    def updown(self, base: str, target: str, name: str):
        """
        This will create a trigger array based on if one point is more than the other.
        """
        base, target = self.adjust_length(base, target)
        triggers = list()
        for bpoint, tpoint in zip(base[1::2], target[1::2]):
            tr = 0
            if bpoint < tpoint:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def crossup(self, base: str, target: str, name: str):
        """
        This is for point alerts when the target trend crosses up on the base trend.
        """
        base, target = self.adjust_length(base, target)
        triggers = list()
        last_points = (0, 0)
        for idx, (bpoint, tpoint) in enumerate(zip(base[1::2], target[1::2])):
            tr = 0
            if idx:
                a, b = last_points
                if a > b and bpoint < tpoint:
                    tr = 1
            last_points = (bpoint, tpoint)
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def crossdown(self, base: str, target: str, name: str):
        """
        This is for point alerts when the target trend crosses up on the base trend.
        """
        base, target = self.adjust_length(base, target)
        triggers = list()
        last_points = (0, 0)
        for idx, (bpoint, tpoint) in enumerate(zip(base[1::2], target[1::2])):
            tr = 0
            if idx:
                a, b = last_points
                if a < b and bpoint > tpoint:
                    tr = 1
            last_points = (bpoint, tpoint)
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def cross_filter(self, crossup: str, crossdown: str, limit: int):
        """
        This will filter false positives out of a pair of one crossup and one crossdown trigger array.
        """
        s = self.style['main']
        np = self.np
        cup, cdown = s[crossup], s[crossdown]
        for idx, (up, down) in enumerate(zip(cup, cdown)):
            if idx < limit:
                start = 0
                stop = idx
            else:
                start = np.subtract(idx, limit)
                stop = idx  # np.subtract(idx, 1)
            if up or down:
                "set both lists [start:stop] to zero"
                block = [0] * int(np.subtract(stop, start))
                cup[start:stop] = block
                cdown[start:stop] = block
        self.style['main'][crossup] = cup
        self.style['main'][crossdown] = cdown
        return self

    def trend(self, target: str, name: str):
        """
        This is for icing alerts to use.
        """
        triggers = list()
        target = self.style['main'][target]
        for point in target[1::2]:
            tr = 0
            if point:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def point_trend(self, target: str, point: float, name: str):
        """
        This is for icing alerts to use.
        """
        triggers = list()
        target = self.style['main'][target]
        for pt in target[1::2]:
            tr = 0
            if pt != point:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self


indicator = Triggers
