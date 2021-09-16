# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import tkinter as tk
import graphiend as gp
from layouts.base import Layout
from utils import config


class Format(Layout):
    """
    This is an example layout format.
    """
    def __init__(self, parent: tk.Frame, cache: gp.ImgCache, settings: config):
        Layout.__init__(self, parent, cache, settings)
