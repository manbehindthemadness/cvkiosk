# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import tkinter as tk
from base import Layout
from utils import config
from graphiend import (
    utils
)


class Body(Layout):
    """
    This is a layout child class that will provide our visual elements for the UX
    """
    def __init__(self, parent: tk.Frame, cache: utils.ImgCache, settings: config):
        Layout.__init__(self, parent, cache, settings)

    def prep(self, style: dict, data: dict):
        """
        This will pass our style configurations down to all out happy little widgets.
        """
        self.style = style
        self.data = data  # Do we need this?
