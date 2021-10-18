# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This provides sound notifications for the units that sport speakers.
"""

import threading
from indicators.base import Indicator
from utils import config

settings = config('settings')


class Alert(Indicator):
    """
    See docstring.
    """
    def __init__(self):
        Indicator.__init__(self)
        if settings['use_sound']:
            from sound import cycle_alert
            self.alert = cycle_alert

        self.alert_triggered = False

    def configure(self, options: [dict, None], style: dict, **kwargs):
        """
        Setup our variables and update matrix solver options.
        """
        self.config(options, style, **kwargs)
        if self.repeat:
            self.alert_triggered = False
        self.source = self.style['main'][self.source]
        return self

    def sound_alert(self):
        """
        This is a threaded wrapper to launch a sound event.
        """
        if self.alert:
            self.alert(self.alert_type)
        return self

    def solve(self):
        """
        Perform actions.
        """
        if self.source[-1] and not self.alert_triggered:
            print('-------------------TRIGGERING ALERT')
            if settings['use_sound']:
                thread = threading.Thread(target=self.sound_alert, args=())
                thread.start()
            self.alert_triggered = True
        else:
            if self.source[-2] and not self.source[-1]:
                print('-------------------RESETTING ALERT')
                self.alert_triggered = False
        return self


indicator = Alert
