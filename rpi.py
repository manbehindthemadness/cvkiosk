# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is where we will put code related to the raspberry pi hardware.
"""

from utils import system_command, percent_in


def wifi_sig() -> int:
    """
    This will read our wifi signal strength.
    """
    cmd = 'iwconfig wlan0 | grep -i --color quality'
    try:
        info = system_command(cmd, shell=True)
        percentages = info.split()[1].split('=')[1]
        a, b = percentages.split('/')
        strength = percent_in(int(a), int(b))
    except FileNotFoundError as err:
        print(err)
        strength = 0
    return strength
