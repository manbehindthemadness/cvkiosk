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
# import numpy as np


class StatBar(tk.Frame):
    """
    This is a status bar designed for the top of our layouts, I supports basic system stats and a configurable
        number of packed labels that can be used for values that don't fit elsewhere.
    """
    style = None
    w_var = tk.IntVar()
    w_lab = None
    b_var = tk.IntVar()
    b_lab = None
    labels = list()

    def __init__(self, parent: tk.Frame):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.b_meter = gp.StatBar(self)
        self.w_meter = gp.StatBar(self)
        self.l_frame = tk.Frame(self)

        self.cr = gp.color_range

    def build_content(self, style):
        """
        This will construct the contents of the widget based on the passed style.
        """