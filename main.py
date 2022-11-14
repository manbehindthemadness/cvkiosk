# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
"""
import threading
from uxutils import setup
from utils import config
from ux import OnScreen
from web import run_dash

config = config('settings')
setup(config)  # Prep environment for display.
web_thread = threading.Thread(target=run_dash, args=(config,), daemon=True)
web_thread.start()
OnScreen().run()
print('done')
