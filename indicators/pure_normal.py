# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is normalized moving average, much like the other indicate this will produce a normalized array; however,
This will use the absolute coords that were scaled with the price matrix, so we don't have scaling problems.

def normalize(c2p, points: np.array, base_spread: int, spread: int, prefix: str = 'raw_', volume: bool = False) -> np.array:

    name = prefix + 'normal_' + str(base_spread) + '_' + str(spread)
    if name in c2p.extras.keys():
        result = c2p.extras[name]
    else:
        ma = ema(c2p, points, base_spread, prefix, volume)
        normal = ema(c2p, points, spread, prefix, volume)
        normal[1::2] = np.subtract(normal[1::2], ma[1::2])
        result = normal
        c2p.extras[name] = normal
    return result
"""

from indicators.base import Indicator


class PureNormal(Indicator):
    """
    feed adjusted exponential moving average.

    TODO: Why on earth does this conflict with the other normal indicator?!
    """

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        mas = self.options['popt']['mas']
        nmas = [self.normal_base, self.normal_spread]
        for ma in nmas:
            if ma not in mas:
                mas.append(ma)
        self.options['popt'].update({'mas': mas})
        self.options['fopt'].update({'mas': mas})
        return self

    def solve(self, *args):
        """
        This will do the actual math and build our solution.
        """
        def normalize(_parent, _source, _base_spread, _spread):
            """
            This will build our normal.
            """
            # Normalize averages.
            _gp = _parent.gp
            _np = _parent.np
            ma = _np.array(_source.extras[str(_base_spread) + '_pure'])
            normal = _np.array(_source.extras[str(_spread) + '_pure'])
            normal[1::2] = _np.subtract(normal[1::2], ma[1::2])  # TODO: Unsure if we should invert this booger.
            # Discover geometry.
            s = _parent.style['main']
            height = s['price_canvas_height']
            lf, rt, tp, bt = s['price_matrix_offsets']
            # Find center points.
            canvas_center = ((height + tp) - (tp + bt)) / 2
            trimmed = _np.array(normal[1::2])  # [-_source.viewable_increment_count:])  # Ensure we are centering on the screen.
            ntp, nbt = trimmed.min(), trimmed.max()
            normal_center = _np.divide(_np.subtract(nbt, ntp), -2)  # TODO: We might need to adjust here as the limits might be positive or negative numbers.
            # Offset normal.
            centers = [normal_center, canvas_center]
            centers.sort()
            centers.reverse()
            master_offset = _np.subtract(*centers)
            normal[1::2] = _np.add(normal[1::2], master_offset)
            normal[0::2] = _np.add(normal[0::2], lf)
            return normal

        pmatrix, fmatrix = args
        source = pmatrix
        if self.source == 'feed':
            source = fmatrix
        normal_name = '_' + self.source + '_pure_normal_' + str(self.normal_base) + '_' + str(self.normal_spread)
        if normal_name not in self.style['main'].keys():  # Ensure we don't re-calculate something we already have.
            self.normal = normalize(self, source, self.normal_base, self.normal_spread)
            self.style['main'][normal_name] = self.normal
        else:
            self.normal = self.style['main'][normal_name]
        solution = self.normal
        self.collect(pmatrix, fmatrix)
        self.solution = solution
        # NOTE: We aren't going to trim this to the view range as we will be using it to attach other trends elsewhere.
        return self


indicator = PureNormal
