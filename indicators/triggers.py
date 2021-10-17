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

    def updown(self, base: str, target: str, name: str):
        """
        This will create a trigger array based on if one point is more than the other.
        """
        s = self.style['main']
        gp = self.gp
        np = self.np
        base, target = np.array(s[base]), np.array(s[target])
        base, target = gp.un_jag([base, target])
        triggers = list()
        for bpoint, tpoint in zip(base[1::2], target[1::2]):
            # print(bpoint, tpoint)
            tr = 0
            if bpoint < tpoint:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self


indicator = Triggers
