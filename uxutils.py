# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
-----------------------------------------------------------------------------------------------------------------------

This is where we will store tkinter related code that is used throughout the various apps.

Scrolling text: https://www.codespeedy.com/move-text-from-right-to-left-in-tkinter/
"""
import time
import os
import tkinter as tk
import numpy as np
from colour import Color
from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)
from utils import (
    percent_of,
    system_command,
    log,
)
from _tkinter import TclError

pys = None


def setup(settings, display_override: str = None):
    """
    This readies our environment for a bar-metal tkinter user interface.
    :param settings: Pass the configs from out app.
    :param display_override: Use this if you want to use an alternative display.
    """

    def dbg(*args):
        """
        ajust a debug return method.
        """
        if settings['debug_startup']:
            log(args)

    dbg('starting display setup', '*dbug*')
    display = settings['display']
    try:
        # This crap is for tunneling the app over ssh
        dbg('setting display variable', '*dbug*')
        os.environ['DISPLAY'] = display
        if not display_override:
            dbg('acquiring Xauth', '*dbug*')
            os.environ['XAUTHORITY'] = '/home/pi/.Xauthority'
            dbg('configuring xhost', '*dbug*')
            system_command(['/usr/bin/xhost', '+'])
            system_command(['echo', '$DISPLAY'])
            if 'localhost' not in display:  # This will disable screen blackouts.
                dbg('configuring display: s off')
                system_command(['xset', 's', 'off', '-display', display])
                dbg('configuring display: -dpms off')
                system_command(['xset', '-dpms', '-display', display])
                dbg('configuring display: noblank on')
                system_command(['xset', 's', 'noblank', '-display', display])
    except (FileNotFoundError, TclError):
        log('local display failed to init, this is usually because we are running in a dev environment')
        os.environ['DISPLAY'] = 'localhost:10.0'
    dbg('display setup complete')


class ScrCap:
    """
    This is a screen capture class that (we hope) will stabalize the wacky failures behind the python screenshot
    libraries.
    """
    def __init__(self, target_file):
        """
        NOTE: This class cannot init until the above 'setup' function has been run.
        """
        self.target_image = target_file
        self.grab = None
        self.imp()

    def imp(self):
        """
        Hopefully imports a screenshot library.
        """
        global pys
        if pys:
            del pys
        import pyscreenshot as pys
        self.grab = pys.grab

    def capture(self, region: tuple):
        """
        Captures and saves a screenshot...hopefully.

        region coords (x1, y1, x2, y2)
        :return:
        """
        try:
            os.remove(self.target_image)
        except FileNotFoundError:
            pass
        while not self.target_image.is_file():
            try:
                img = self.grab(bbox=region)
                img.save(self.target_image)
            except self.grab.err.FailedBackendError:  # pyscreenshot.err.FailedBackendError
                pass
            if not self.target_image.is_file():
                print('capture failed', '*warn*')
                self.imp()
                time.sleep(0.5)

    def enhance(self):
        """
        Color corrrects from the LCD to something more appealing on a browser.
        """
        img = Image.open(self.target_image)
        converter = ImageEnhance.Color(img)
        img = converter.enhance(2.0)
        img = img.filter(ImageFilter.SHARPEN)
        img.save(self.target_image)


def from_rgb(rgb: tuple) -> str:
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def color_range(limit_low: int, limit_high: int, from_color: str, to_color: str) -> list:
    """
    This converts a number into an RGB tuple this it defined within the limits
    """
    limit_high += 1
    fcolor = Color(from_color)
    values = list()
    colors = list(fcolor.range_to(Color(to_color), abs(limit_high - limit_low)))
    for color in colors:
        values.append(Color.get_hex(color))
    return values


class StatBar(tk.Frame):
    """
    This is a percentage (0-100) statictic bar-meter
    """
    def __init__(
            self,
            parent: tk.Frame,
    ):
        tk.Frame.__init__(self)
        self.parent = parent
        self.hist = list()
        self.vertical = None
        self.width = None
        self.height = None
        self.background = None
        self.text_color = None
        self.border = None
        self.border_color = None
        self.meter_color = None
        self.meter_colors = None
        self.meter_border_color = None
        self.meter_border = None
        self.meter_var = None
        self.meter_label = None
        self.meter_label_width = None
        self.base = tk.Frame(self)
        self.meter = tk.Frame(self.base)
        self.label_frame = tk.Frame(self.base)
        self.label = tk.Label(self.label_frame)
        self.meter_text = tk.StringVar()
        self.old_value = None
        self.val_override = None
        self.font_override = None
        self.average = None

    def color_finder(self):
        """
        This allows us to select nifty colors in an array for the bars.
        """
        if self.meter_colors:
            self.meter_color = self.meter_colors[int(self.meter_var.get())]
        return self

    def value_finder(self):
        """
        This takes the string from our meter label and adds the meter_value.
        """
        prefix = self.meter_label
        if self.val_override:
            prefix = self.val_override
        value = prefix + ': ' + str(np.round(self.meter_var.get(), 2))
        self.meter_text.set(value)
        return self

    def refresh(self):
        """
        This will refresh our meter and variable values.
        """
        value = self.meter_var.get()
        if self.average:
            self.hist.append(value)
            self.hist = self.hist[-self.average:]
            value = float(np.average(self.hist))
            self.meter_var.set(value)
        if value != self.old_value:  # Only update if we need to.
            self.params(
                update=True
            )
            self.old_value = value

    def params(
            self,
            vertical: bool = None,
            width: int = 100,
            height: int = 100,
            background: [str, tuple] = 'black',
            text_color: [str, tuple] = 'white',
            border: int = 0,
            border_color: [str, tuple] = 'black',
            meter_color: [str, tuple] = 'green',
            meter_colors: list = None,
            meter_border: int = 0,
            meter_border_color: [str, tuple] = 'black',
            meter_var: [tk.DoubleVar, tk.IntVar] = None,
            meter_label: str = None,
            meter_label_width: int = None,
            update: bool = False,
            val_override: str = None,
            font_override: str = None,
            average_samples: int = None,
    ):
        """
        This configures our various visuals

        Note: When meter_colors is specified it will remove the meter_color value.
                Also meter_colors must be in a list of 100 shades of colors for a transition.

        Note: Take note that this is designed to operate on a percentage from 0-100.
        """
        if not update:
            self.vertical = vertical  # The orientation of the meter bar
            self.width = width
            self.height = height
            self.background = background
            self.text_color = text_color
            self.border = border
            self.border_color = border_color
            self.meter_color = meter_color
            self.meter_colors = meter_colors
            self.meter_border_color = meter_border_color
            self.meter_border = meter_border
            self.meter_label = meter_label
            self.meter_label_width = meter_label_width
            self.meter_var = meter_var
            self.val_override = val_override
            self.font_override = font_override
            self.average = average_samples

        static_height = 10

        if self.vertical:
            anchor = 'center'
            dynamic_height = percent_of(self.meter_var.get(), np.subtract(self.height, static_height))
            lbl_height = static_height
            lbl_width = self.width
            lbl_x = 0
            lbl_y = np.subtract(self.height, static_height)
            pad_x = 0
            pad_y = 0
            mtr_height = int(self.meter_var.get())
            mtr_width = self.width
            mtr_x = 0
            mtr_y = np.subtract(np.subtract(self.height, static_height), dynamic_height)
        else:
            anchor = 'w'
            dynamic_width = percent_of(self.meter_var.get(), np.subtract(self.width, self.meter_label_width))
            lbl_height = self.height
            lbl_width = self.meter_label_width
            lbl_x = 0
            lbl_y = 0
            pad_x = 2
            pad_y = 0
            mtr_height = self.height
            mtr_width = dynamic_width
            mtr_x = self.meter_label_width
            mtr_y = 0

        if not update:
            self.base.configure(
                bg=self.background,
                highlightthickness=self.border,
                highlightcolor=self.border_color,
            )
            self.base.place(
                x=0,
                y=0,
                width=self.width,
                height=self.height
            )

            self.label_frame.place(
                x=lbl_x,
                y=lbl_y,
                width=lbl_width,
                height=lbl_height,
            )
            ft = ("Helvetica", 6)
            if self.font_override:
                ft = self.font_override
            self.label.configure(
                bg=self.background,
                font=ft,
                fg=self.text_color,
                padx=pad_x,
                pady=pad_y,
                textvariable=self.meter_text,
                anchor=anchor
            )
            self.label.place(
                x=0,
                y=0,
                width=lbl_width,  # Move to place.
                height=lbl_height,
            )
        self.color_finder()  # Update meter color depending.
        self.meter.configure(
            bg=self.meter_color,
            highlightthickness=self.meter_border,
            highlightcolor=self.meter_border_color,
        )
        self.meter.place(
            x=mtr_x,
            y=mtr_y,
            height=mtr_height,
            width=mtr_width
        )
        self.value_finder()  # Update the label text.
        # self.update()
        return self


class EventLog(tk.Frame):
    """
    This is a simple event log that will deliver messages in 10 pixel lines with configurable length
        and number of lines displayed. These lines are expected in list format.
    """
    def __init__(self, parent):
        tk.Frame.__init__(self)
        self.parent = parent
        self.width = None
        self.lines = None
        self.background = None
        self.text_color = None
        self.border_color = None
        self.border_width = None
        self.base = tk.Frame(self)
        self.values = None
        self.stringvars = None
        self.labels = None
        self.old_values = None
        self.maxlen = None
        self.font_override = None

    def make_lines(self):
        """
        This ensures that our text content will fit the box.
        """
        if self.values != self.old_values:  # Only update if we need to.
            self.values = self.values[-self.lines:]
            if len(self.values) < self.lines:
                padding = [str()] * int((np.subtract(self.lines, len(self.values))))
                self.values.extend(padding)
            for idx, value in enumerate(self.values):
                if len(value) > self.maxlen:
                    value = value[:int(np.subtract(self.maxlen, 3))] + '...'
                self.stringvars[idx].set(value.upper())
            self.old_values = self.values
        return self.values

    def refresh(self, values: list = None):
        """
        Updates the contents of the log.
        """
        if values:
            self.values = values
        result = self.make_lines()
        return result

    def params(
            self,
            width: int = 100,
            lines: int = 10,
            values: list = None,
            background: str = 'black',
            text_color: str = 'white',
            border_color: str = 'black',
            border_width: int = 0,
            font_override: str = None
    ):
        """
        This configures the various bits we will use.
        """
        self.width = width
        self.lines = lines
        self.values = values
        self.background = background
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.font_override = font_override

        self.stringvars = list()
        for idx in range(0, self.lines):
            exec('self.sv' + str(idx) + ' = tk.StringVar()')
            exec('self.stringvars.append(self.sv' + str(idx) + ')')
        height = np.multiply(self.lines, 10)
        self.base.configure(
            bg=self.background,
            highlightthickness=self.border_width,
            highlightcolor=self.border_color,
        )
        self.base.place(
            x=0,
            y=0,
            width=self.width,
            height=height,
        )
        self.maxlen = np.subtract(np.round(np.divide(self.width, 4.3), 0), 1)  # noqa
        self.make_lines()
        self.labels = list()
        for idx, line in enumerate(self.stringvars):
            lbl = tk.Label(self.base)
            fnt = ("Helvetica", 6)
            if self.font_override:
                fnt = self.font_override
            lbl.configure(
                bg=self.background,
                fg=self.text_color,
                font=fnt,
                textvariable=line,
                anchor='w'
            )
            lbl.place(
                x=0,
                y=np.multiply(idx, 10),
                width=self.width,
                height=10
            )
            self.labels.append(lbl)
            self.update()
        return self
