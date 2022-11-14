# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
This is where we will put code related to the raspberry pi hardware.
"""

from utils import system_command, percent_in, config


settings = config('settings')
skip = False


def wifi_sig() -> int:
    """
    This will read our wifi signal strength.
    """
    global skip
    cmd = 'iwconfig wlan0 | grep -i --color quality'
    strength = 0
    if not skip:
        try:
            info = system_command(cmd, shell=True)
            percentages = info.split()[1].split('=')[1]
            a, b = percentages.split('/')
            strength = percent_in(int(a), int(b))
        except (FileNotFoundError, IndexError) as err:
            if settings['debug_startup']:
                print(err)
            skip = True

    return strength
