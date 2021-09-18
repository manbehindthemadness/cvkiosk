# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
# import threading
from utils import config
from ux import OnScreen

config = config('settings')
oc = OnScreen(debug_mode=True)
oc.run()
