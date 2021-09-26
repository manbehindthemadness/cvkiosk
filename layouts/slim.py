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
        self.widgets = [  # This is the list of included widgets for this layout,
            'smoothi_bottom',
            'smoothi_top',
            'volume',
            'top_arrows',
            'bottom_arrows',
            'candlesticks',
            'icing_top1',
            'icing_top2',
            'icing_bottom1',
            'tics1',
            'date_ruler',
            'tics2',
            'statbar',
            'ticker'
        ]
        self.labelvars = {  # This specifies the extra labels to be included in the statbar.
            'UTC': tk.StringVar(),
            'FGI': tk.StringVar(),
            'QUO': tk.StringVar(),
        }

