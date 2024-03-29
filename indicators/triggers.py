# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales
------------------------------------------------------------------------------------------------------------------------
This is a unique indicator that need to be run LAST. This is because it requires the output of the other indicators to
    already be solved in order to work.

TODO: We may want to reverse some of these indicators depending on the FGI.

IMPORTANT, the trigger arrays are in the order of the candlesticks first being the oldest last newest.
"""

from indicators.base import Indicator
from utils import get_median


class Triggers(Indicator):
    """
    See docstring
    """
    colors = dict()
    color_ranges = dict()
    triggers = dict()
    pmatrix = None
    fmatrix = None

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        self.pmatrix, self.fmatrix = args
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

    def updown(self, base: str, target: str, name: str, transform: bool = False):
        """
        This will create a trigger array based on if one point is more than the other.
        """
        def tf(arry):
            """
            This will handle array transformations from non-pixel coordinates.
            """
            np = self.np
            vic = self.pmatrix.viewable_increment_count
            pts = np.array(arry)
            pts[1::2] = np.multiply(pts[1::2], -1)
            pmin = np.amin(pts[1::2][-vic:])
            pts[1::2] = np.subtract(pts[1::2], pmin)
            pts[1::2] = gp.zero_v_scale(
                pts[1::2],
                200,
                vic
                )
            return pts

        base, target = self.adjust_length(base, target)
        if transform:
            gp = self.gp
            base, target = tf(base), tf(target)
        triggers = list()
        for bpoint, tpoint in zip(base[1::2], target[1::2]):
            tr = 0
            if bpoint < tpoint:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def crossup(self, base: str, target: str, name: str, rad: int = 1):
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
                if a >= b and bpoint < tpoint:
                    tr = rad
            last_points = (bpoint, tpoint)
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def crossdown(self, base: str, target: str, name: str, rad: int = 1):
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
                if a <= b and bpoint > tpoint:
                    tr = rad
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
        cup, cdown = s[crossup], s[crossdown]  # TODO: Verify these are being passed properly...
        cup_invalid, cdown_invalid = list(cup), list(cdown)  # Collect invalidated signals.
        for idx, (up, down) in enumerate(zip(cup, cdown)):
            if idx < limit:
                start = 0
                stop = idx
            else:
                start = np.subtract(idx, limit)
                stop = idx
            if up or down:
                "set both lists [start:stop] to zero"
                block = [0] * int(np.subtract(stop, start))
                cup[start:stop] = block
                cdown[start:stop] = block
                if up and down:  # Prevent conflicts.
                    cup[idx] = cdown[idx] = 0
        # Collect the invalidated signals.
        for idx, (inval_up, inval_down, val_up, val_down) in enumerate(zip(cup_invalid, cdown_invalid, cup, cdown)):
            if inval_up and val_up:
                cup_invalid[idx] = 0
            if inval_down and val_down:
                cdown_invalid[idx] = 0
        # TODO: We need to gather information for the trading bot here.
        self.style['main'][crossup] = cup
        self.style['main'][crossup + '_invalid'] = cup_invalid
        self.style['main'][crossdown] = cdown
        self.style['main'][crossdown + '_invalid'] = cdown_invalid
        self.log_alert(self.kwargs['crossup'], cup)
        self.log_alert(self.kwargs['crossdown'], cdown)
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

    def point_trend(self, target: str, name: str):
        """
        This is for icing alerts to use.
        """

        triggers = list()
        target = self.style['main'][target]
        point = get_median(target)
        for pt in target[1::2]:
            tr = 0
            if pt and pt != point:
                tr = 1
            triggers.append(tr)
        self.style['main'][name] = triggers
        return self

    def hybrid_scale(self, averages: list, lengths: tuple, name: str):
        """
        This will take two foreign graphs and scale them into mutual coordinates that can be used by the other triggers.
        """
        gp = self.gp
        np = self.np
        source = self.pmatrix

        height = 1000

        self.averages = list()
        for ave in averages:
            self.averages.append(self.style['main'][ave])
        self.averages = gp.un_jag(self.averages)  # Remove jagged arrays.
        self.averages = np.array(self.averages)
        self.averages = gp.macd(source, lengths, self.averages[:, 1::2])  # Send only the Y coords.

        self.averages = self.averages[:, -source.viewable_increment_count * 2:]  # Cut to view.
        positive_shift = np.amin(self.averages[:, 1::2])
        self.averages[:, 1::2] = np.subtract(self.averages[:, 1::2], positive_shift)  # Bring us back to positive.
        ave_ys = gp.zero_v_scale_matrix(
            self.averages[:, 1::2],
            height,
            source.viewable_increment_count + 2
            )  # Get Y coords.
        self.averages[:, 1::2] = ave_ys
        self.averages = list(self.averages)
        del self.averages[0]  # Remove flat line.

        if name + '_0' not in self.style['main'].keys():  # Update style.
            eg_1 = self.averages[0]
            eg_2 = self.averages[1]
            self.style['main'][name + '_1'] = eg_1
            self.style['main'][name + '_2'] = eg_2

        return self


indicator = Triggers
