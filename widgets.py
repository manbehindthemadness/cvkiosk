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
import numpy as np


class StatBar(tk.Frame):
    """
    This is a status bar designed for the top of our layouts, I supports basic system stats and a configurable
        number of packed labels that can be used for values that don't fit elsewhere.
    """
    init = True
    style = None
    w_var = tk.IntVar()
    w_lab = None
    b_var = tk.IntVar()
    b_lab = None
    vars = None
    text = None
    labels = None
    show_labels = None

    def __init__(self, parent: tk.Frame):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.b_meter = gp.StatBar(self)
        self.w_meter = gp.StatBar(self)
        self.l_frame = tk.Frame(self)

        self.cr = gp.color_range

    def build_content(self, **style):
        """
        This will construct the contents of the widget based on the passed style.
        """
        if self.init:
            s = self.style = style

            self.vars = s['vars']
            self.labels = s['labels']
            self.text = s['text']
            self.show_labels = s['extra_labels']

            x, y = s['coords']
            self.configure(
                bg=s['background'],
                border=s['border']
            )
            self.place(
                x=x,
                y=y,
                width=s['width'],
                height=s['height']
            )
            d_width = np.divide(s['width'], len(self.vars))
            self.b_meter.params(  # Battery meter.
                width=d_width,
                height=s['height'],
                background=s['background'],
                # background='green',
                text_color=s['text_color'],
                border=s['border'],
                meter_colors=s['meter_colors_left'],
                meter_border=s['border'],
                meter_var=self.vars[0],
                meter_label=self.text[0],
                meter_label_width=s['meter_label_width_left'],
                font_override=s['font'],
                average_samples=s['average']
            )
            self.b_meter.place(
                x=x,
                y=y,
                width=d_width,
                height=s['height'],
            )
            w_x = np.multiply(d_width, np.subtract(len(self.vars), 1))
            self.w_meter.params(  # Wifi Meter.
                mirror=True,
                width=d_width,
                height=s['height'],
                background=s['background'],
                # background='blue',
                text_color=s['text_color'],
                border=s['border'],
                meter_colors=s['meter_colors_right'],
                meter_border=s['border'],
                meter_var=self.vars[1],
                meter_label=self.text[1],
                meter_label_width=s['meter_label_width_right'],
                font_override=s['font'],
                average_samples=s['average']
            )
            self.w_meter.place(
                x=w_x,
                y=y,
                width=d_width,
                height=s['height'],
            )
        self.init = False

    def animate(self):
        """
        This is a dummy so we work with the layout main logic.
        """
        return self

