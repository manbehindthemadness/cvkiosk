# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is the base indicator class.
"""

import graphiend as gp
import numpy as np
from utils import get_args


class Indicator:
    """
    Inherited base indicator class.
    """
    name = None
    source = None

    matrix_override = list()

    options = None
    normal_base = None
    normal_spread = None
    ema_spread = None
    obv_spread = None
    faobv_spread = None
    history = None
    alert = None
    alert_type = None
    repeat = None

    solution = None
    triggers = None
    normal = None
    drift = None
    ma = None
    dd = None
    polarity = None

    kw = [
        'normal_base',
        'normal_spread',
        'ema_spread',
        'obv_spread',
        'faobv_spread',
        'source',
        'polarity',
        'matrix_override',
        'alert_type',
        'repeat'
    ]

    def_options = {
        'popt': {  # Price matrix options.
            'mas': list(),
            'vas': list(),
            'macd': False,
            'obv': False
        },
        'fopt': {  # Feed matrix options.
            'mas': list(),
            'vas': list(),
            'macd': False,
            'obv': False
        },
    }

    def __init__(self):
        self.style = None
        self.kwargs = None
        self.gp = gp
        self.np = np
        self.ga = get_args

    def config(self, options: [dict, None], style: dict, **kwargs):
        """
        Populates our variables.

        We will call this in the child classes configure method so we can pass back the matrix solver options.
        """
        if not options:
            options = self.def_options  # we do this so we can pass the options to all indicators in a chain.
        self.options = options
        self.style = style
        self.kwargs = kwargs
        cmd = str()
        for kw in self.kw:
            cmd += 'self.' + kw + ', '
        cmd += ' = get_args(self.kw, self.kwargs)'
        exec(cmd)
        if not self.matrix_override:
            self.matrix_override = list()
        else:
            self.matrix_override = np.array(self.matrix_override)
        return self

    def collect(self, pmatrix, fmatrix):
        """
        This will collect all the extra processed coordinate streams in the ChartToPix instances and add them into
            our style so they can be called by the widgets.
        """

        def itr(ext: dict, prefix: str) -> dict:
            """
            This will pull out our keys and get them ready to update the style.
            """
            result = dict()
            for value in ext:
                if value in ['mas', 'vas']:
                    pref = value
                    for sub_value in ext[value]:
                        result[prefix + pref + '_' + sub_value] = np.array(ext[value][sub_value])
                else:
                    result[prefix + value] = np.array(ext[value])
            return result

        pextras, fextras = pmatrix.extras, fmatrix.extras
        self.style['main'].update(itr(pextras, 'price_'))
        self.style['main'].update(itr(fextras, 'feed_'))
        return self


class Dummy(Indicator):
    """
    This is a dummy class so the IDE can see pas the exec statements.
    """

    def __init__(self):
        Indicator.__init__(self)

    def configure(self, options: [dict, None], style: dict, **kwargs):  # noqa
        """
        Setup our variables and update matrix solver options.
        """
        return self

    def solve(self, *args):  # noqa
        """
        This will do the actual math and build our solution.
        """
        return self
