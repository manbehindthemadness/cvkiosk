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
    labels = None
    show_labels = None

    def __init__(self, parent: tk.Frame, base):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.base = base
        self.b_meter = gp.StatBar(self)
        self.w_meter = gp.StatBar(self)
        self.l_frame = tk.Frame(self)

        self.statbars = [
            self.b_meter,
            self.w_meter
        ]
        self.cr = gp.color_range

    def build_content(self, **style):
        """
        This will construct the contents of the widget based on the passed style.
        """
        s = self.style = style

        self.labels = self.base.labels  # noqa

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
        d_width = int(np.divide(s['width'], len(self.base.labels)))
        self.b_meter.params(  # Battery meter.
            width=d_width,
            height=s['height'],
            background=s['background'],
            text_color=s['text_color'],
            border=s['border'],
            meter_colors=s['meter_colors_left'],
            meter_border=s['border'],
            meter_var=self.base.labels['BAT'],
            meter_label='BAT',
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
        w_x = int(np.multiply(d_width, np.add(len(self.base.labels), -1)))
        self.w_meter.params(  # Wifi Meter.
            mirror=True,
            width=d_width,
            height=s['height'],
            background=s['background'],
            text_color=s['text_color'],
            border=s['border'],
            meter_colors=s['meter_colors_right'],
            meter_border=s['border'],
            meter_var=self.base.labels['WFI'],
            meter_label='WFI',
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
        for idx, label in enumerate(self.base.labels):
            if label not in ['WFI', 'BAT']:
                exec('self.' + label + ' = tk.StringVar()')
                exec('self.' + label + '.set("' + label + ': 0")')

                lbl = tk.Label(self)
                lbl.configure(
                    bg=s['background'],
                    fg=s['text_color'],
                    font=s['font'],
                    border=s['border'],
                    width=d_width,
                    height=s['height'],
                    textvar=eval('self.' + label)
                )
                x = int(np.multiply(d_width, np.add(idx, 1)))
                lbl.place(
                    x=x,
                    y=y,
                    width=d_width,
                    height=s['height'],
                )
                exec('self.' + label + '_label = lbl')
        return self

    def refresh(self):
        """
        This will refresh our contents.
        """
        for sbar in self.statbars:
            sbar.refresh()

    def animate(self):
        """
        This is a dummy so we work with the layout main logic.
        """
        return self

