# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is the base indicator class.
"""
import datetime
import graphiend as gp
import numpy as np
from utils import get_args
from mergedeep import merge
# from collections import OrderedDict


LOGGED_ALERTS = dict()
LOGGED_NOTIFICATIONS = list()


class Indicator:
    """
    Inherited base indicator class.
    """
    enable_log_alerts = False

    name = None
    source = None
    source_type = None

    matrix_override = list()
    overrides = dict()

    averages = None
    options = None
    normal_base = None
    normal_spread = None
    ema_spread = None
    obv_spread = None
    faobv_spread = None
    guides = None
    history = None
    alert = None
    alert_type = None
    repeat = None

    suffix = None

    solution = None
    triggers = None
    normal = None
    drift = None
    ma = None
    dd = None
    polarity = None

    kw = [
        'averages',
        'overrides',
        'normal_base',
        'normal_spread',
        'ema_spread',
        'obv_spread',
        'faobv_spread',
        'source',
        'source_type',
        'polarity',
        'matrix_override',
        'alert_type',
        'repeat',
        'suffix',
        'guides',
        'log_alerts',  # This is for the alerts we will send over to Denniks.
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
        if 'log_alerts' in self.kwargs.keys():
            if self.kwargs['log_alerts']:
                self.enable_log_alerts = True
            del self.kwargs['log_alerts']
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
            our style, so they can be called by the widgets.
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

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        This is a dummy method used for options overrides.
        """
        self.config(options, style, **kwargs)
        self.options = merge(self.options, self.overrides)
        return self

    def solve(self, *args):
        """
        This is a dummy method used for options overrides.
        """
        self.collect(*args)
        return self

    def log_alert(self, name: str, triggers: list):
        """
        This will add an entry into the logged_alerts cache, so we can evaluate it remotely.

        from collections import OrderedDict

        # create an OrderedDict with some unsorted data
        data = OrderedDict([('apple', 10), ('orange', 5), ('banana', 20)])

        # sort the OrderedDict by value (in ascending order)
        sorted_data = OrderedDict(sorted(data.items(), key=lambda x: x[1]))

        print(sorted_data)
        # Output: OrderedDict([('orange', 5), ('apple', 10), ('banana', 20)])


        Data Model:

        {
            <alert_name>: [<timestamp>, ...]
        }

        """
        global LOGGED_ALERTS
        global LOGGED_NOTIFICATIONS
        if self.enable_log_alerts and name not in LOGGED_NOTIFICATIONS:
            print(f'logging enabled on {name}')
            LOGGED_NOTIFICATIONS.append(name)
        if self.enable_log_alerts and triggers[-1]:
            now = datetime.datetime.now()
            rounded_minute = (now.minute // 15) * 15
            stamp = str(now.replace(minute=rounded_minute, second=0, microsecond=0))
            if name not in LOGGED_ALERTS.keys():
                LOGGED_ALERTS[name] = list()
            if stamp not in LOGGED_ALERTS[name]:
                print(f'logging alert: {name}, {stamp}')
                LOGGED_ALERTS[name].append(stamp)
        return self


class Dummy(Indicator):
    """
    This is a dummy class so the IDE can see pas the exec statements.
    """
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


indicator = Indicator
