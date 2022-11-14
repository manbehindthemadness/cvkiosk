# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is feed adjusted exponential moving average; however,
This will use the absolute coords that were scaled with the price matrix, so we don't have scaling problems.

def cross_normalize(
        c2p, normal: np.array, points: np.array,
        spread: int = 26, prefix: str = 'raw_',
        volume: bool = False) -> np.array:
)
    name = prefix + 'cross_normal_' + str(spread)
    if name in c2p.extras.keys():
        result = convert_to_pixels(c2p, c2p.extras[name])
    else:
        _ema = ema(c2p, points, spread, prefix, volume)
        cross = np.array(normal)
        cross[1::2] = np.add(_ema[1::2], cross[1::2])
        result = center(c2p, cross, _ema)
        c2p.extras[name] = result
    return result
"""

from indicators.base import Indicator
from indicators.pure_normal import PureNormal
norm = PureNormal()


class PureFAEMA(Indicator):
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
        def cross_normalize(_parent, _pmatrix, _normal, _ema_spread):
            """
            This will center the normal at zero and then modify the pure ema accordingly.
            """
            _np = _parent.np
            _normal_y = _np.array(_normal[1::2])
            nbt, ntp = _normal_y.max(), _normal_y.min()
            normal_center = _np.add(ntp, _np.divide(_np.subtract(nbt, ntp), 2))
            centered_normal = _np.subtract(_normal_y, normal_center)
            ema = _np.array(_pmatrix.extras[str(_ema_spread) + '_pure'])
            ema[1::2] = _np.add(ema[1::2], centered_normal)
            # Apply offsets.
            lf, rt, tp, bt = _parent.style['main']['price_matrix_offsets']
            ema[1::2] = _np.add(ema[1::2], tp)
            ema[0::2] = _np.add(ema[0::2], lf)
            return ema

        pmatrix, fmatrix = args
        name = '_pure_faema_' + str(self.normal_base) + '_' + str(self.normal_spread) + '_' + str(self.ema_spread)
        if name not in self.style['main'].keys():
            norm.solve(*args)
            self.normal = norm.solution
            solution = cross_normalize(self, pmatrix, self.normal, self.ema_spread)
            self.style['main'][name] = solution
        else:
            solution = self.style['main'][name]
        self.collect(pmatrix, fmatrix)
        self.solution = solution
        # NOTE: We aren't going to trim this to the view range as we will be using it to attach other trends elsewhere.
        return self


indicator = PureFAEMA
