# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import threading
from utils import config
from ux import OnScreen
from web import run_dash

config = config('settings')
web_thread = threading.Thread(target=run_dash, args=(config,))
web_thread.start()
oc = OnScreen()
oc.run()
print('done')
