# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import os
import shutil
import tkinter as tk
import graphiend as gp
import numpy as np
from utils import config
from pathlib import Path
from PIL import Image, ImageTk


settings = config('settings')


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
    labelvars = None
    show_labels = None
    lbls = list()

    def __init__(self, parent: tk.Frame, base):
        tk.Frame.__init__(self)
        self.parent = parent
        self.base = base
        self.b_meter = gp.StatBar(self)
        self.w_meter = gp.StatBar(self)

        self.statbars = [
            self.b_meter,
            self.w_meter
        ]
        self.cr = gp.color_range

    @staticmethod
    def create_or_modify(i: int, arry: list, *args, **kwargs):
        """
        This will update an existing label, if the label does not exist, it will create a new one.
        """
        try:
            lbl = arry[i]
        except IndexError:
            lbl = tk.Label(*args, **kwargs)
            arry.append(lbl)
            lbl.pack(side=tk.LEFT)
        return lbl

    def build_content(self, **style):
        """
        This will construct the contents of the widget based on the passed style.
        """
        s = self.style = style

        self.labelvars = self.base.labelvars  # noqa

        x, y = s['coords']
        self.configure(
            bg=s['background'],
            border=s['border'],
            width=s['width'],
            height=s['height']
        )
        self.place(
            x=x,
            y=y,
            width=s['width'],
            height=s['height']
        )
        d_width = int(np.divide(s['width'], len(self.base.labelvars)))
        self.b_meter.params(  # Battery meter.
            width=d_width,
            height=s['height'],
            background=s['background'],
            text_color=s['text_color'],
            border=s['border'],
            meter_colors=s['meter_colors_left'],
            meter_border=s['border'],
            meter_var=self.base.labelvars['BAT'],
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
        w_x = int(np.multiply(d_width, np.add(len(self.base.labelvars), -1)))
        self.w_meter.params(  # Wifi Meter.
            mirror=True,
            width=d_width,
            height=s['height'],
            background=s['background'],
            text_color=s['text_color'],
            border=s['border'],
            meter_colors=s['meter_colors_right'],
            meter_border=s['border'],
            meter_var=self.base.labelvars['WFI'],
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
        for idx, label in enumerate(self.base.labelvars):
            if label not in ['WFI', 'BAT']:
                exec('self.' + label + ' = tk.StringVar()')
                exec('self.' + label + '.set("' + label + ': 0")')

                lbl = self.create_or_modify(idx, self.lbls, self, height=s['height'], width=d_width)
                tvar = eval('self.' + label)
                lbl.configure(
                    bg=s['background'],
                    fg=s['text_color'],
                    font=s['font'],
                    border=s['border'],
                    width=d_width,
                    height=s['height'],
                    textvar=tvar
                )
                x = int(np.multiply(d_width, np.add(idx, 1)))
                lbl.place(
                    x=x,
                    y=y,
                    width=d_width,
                    height=s['height'],
                )
                exec('self.' + label + '_label = lbl')
        self.update()
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


class Faker:
    """
    This is a sneaky technique to use a screenshot to hide the redraw whilst loading process.
    """
    def __init__(self, parent, layout):
        self.parent = parent
        self.layout = layout
        self.coords = None
        self.frame = None
        self.canvas = None

        self.cap_source = Path('www/chart.png')
        self.cap_target = self.cap_source
        self.cap = None

    def show(self):
        """
        This will copy the screen cap file, set it as our background and raise the frame to cover the
            price canvas.
        """
        if settings['use_faker']:
            x1 = self.layout.winfo_x()
            y1 = self.layout.winfo_y()
            x2 = np.add(x1, self.layout.winfo_width())
            y2 = np.add(y1, self.layout.winfo_height())
            self.coords = (x1, y1, x2, y2,)
            print(self.coords)
            if self.cap_source.is_file():
                with open(self.cap_target, 'rb', 0) as file:
                    cap = Image.open(file)
                    cap.load()
                    file.close()
                    del file
                self.cap = ImageTk.PhotoImage(cap)

                self.frame = tk.Frame()
                self.frame.configure(
                    width=x2,
                    height=y2,
                    bd=0,
                    highlightthickness=0
                )
                self.frame.place(
                    x=x1,
                    y=y1,
                    width=x2,
                    height=y2
                )
                self.canvas = tk.Canvas(self.frame)
                self.canvas.configure(
                    width=x2,
                    height=y2,
                    bd=0,
                    highlightthickness=0
                )
                self.canvas.place(
                    x=0,
                    y=0,
                    width=x2,
                    height=y2
                )

                self.canvas.create_image((0, 0), image=self.cap, anchor='nw')
                self.frame.tkraise()
                # print('raising self')
            else:
                print('capture not found')
        return self

    def hide(self):
        """
        This will remove our capture and raise the parent.
        """
        if settings['use_faker']:
            try:
                self.frame.destroy()
                gp.burn(self.cap)
                self.canvas.destroy()
            except AttributeError:
                pass
            # print('killing self')
        return self
