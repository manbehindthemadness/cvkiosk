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
            'shmacd',
            'smoothi_bottom',
            'smoothi_bottom_backdrop',
            'smoothi_top_backdrop',
            'smoothi_top',
            'volume',
            'top_arrows',
            'top_arrows_invalid',
            'bottom_arrows',
            'bottom_arrows_invalid',
            'candlesticks',
            'icing_top1',
            'icing_top2',
            'icing_bottom1',
            'icing_bottom2',
            'onions1',
            'points1',
            'points2',
            'line1',
            'line2',
            'line3',
            'tics1',
            'date_ruler',
            'tics2',
            'statbar',
            'ticker'
        ]
        self.labelvars = {  # This specifies the extra labels to be included in the statbar.
            'TIK': tk.StringVar(),
            'FGI': tk.StringVar(),
            'QUO': tk.StringVar(),
        }
