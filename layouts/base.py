# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

In this we will pass two dictionaries data and style.
In the data dictionary we will have our tk.Xvar elements that will be passed to their respective labels via key to
    name matching.
In the style dictionary we will pass visual configurations key-named to their respective widgets.

TODO: It's become evident that we are evaluating widgets that aren't in the layout properly during draw...
"""
import tkinter as tk
import graphiend as gp
from utils import config
from widgets import StatBar


class Layout(gp.Diagram):
    """
    This is the base layout class for the various user interface configurations.
    """
    first = True

    style = dict()
    data = dict()

    widgets = list()
    labelvars = dict()

    def __init__(self, parent: tk.Frame, cache: gp.ImgCache, settings: config):
        """
        Basically we are going to init all the visual elements we plan to use here and just call them when needed.
        """
        gp.Diagram.__init__(self, parent)
        self.parent = parent
        self.cache = cache
        self.config = settings
        self.assets = list()  # Visual assets
        self.asset = None
        self.actors = list()  # Active elements (moving).
        self.actor = None
        self.style = None

        # Get widgets.

        self.candlesticks = gp.CandleSticks(self, cache)
        self.smoothi_top = gp.SmoothiVolumeH(self, cache)
        self.smoothi_bottom = gp.SmoothiVolumeH(self, cache)
        self.smoothi_top_backdrop = gp.SmoothiVolumeH(self, cache)
        self.smoothi_top_backdrop_shadow = gp.SmoothiVolumeH(self, cache)
        self.smoothi_bottom_backdrop = gp.SmoothiVolumeH(self, cache)
        self.smoothi_bottom_backdrop_shadow = gp.SmoothiVolumeH(self, cache)
        self.schematic = gp.SchematicRuler(self, cache)
        self.schematic_tics = gp.TicArray(self)
        self.volume = gp.SpikyVolumeH(self, cache)
        self.top_arrows = gp.ArrowAlert(self, cache)
        self.bottom_arrows = gp.ArrowAlert(self, cache)
        self.top_arrows_invalid = gp.ArrowAlert(self, cache)
        self.bottom_arrows_invalid = gp.ArrowAlert(self, cache)
        self.onions1 = gp.OnionRingAlert(self, cache)
        self.onions2 = gp.OnionRingAlert(self, cache)
        self.onions3 = gp.OnionRingAlert(self, cache)
        self.icing_top1 = gp.IcingAlert(self, cache)
        self.icing_top2 = gp.IcingAlert(self, cache)
        self.icing_top3 = gp.IcingAlert(self, cache)
        self.icing_bottom1 = gp.IcingAlert(self, cache)
        self.icing_bottom2 = gp.IcingAlert(self, cache)
        self.icing_bottom3 = gp.IcingAlert(self, cache)
        self.line1 = gp.Line(self, cache)
        self.line2 = gp.Line(self, cache)
        self.line3 = gp.Line(self, cache)
        self.line4 = gp.Line(self, cache)
        self.points1 = gp.PointAlert(self, cache)
        self.points2 = gp.PointAlert(self, cache)
        self.points3 = gp.PointAlert(self, cache)
        self.points4 = gp.PointAlert(self, cache)
        self.price_ruler = gp.PriceRuler(self, cache)
        self.tics1 = gp.TicArray(self)
        self.tics2 = gp.TicArray(self)
        self.tics3 = gp.TicArray(self)
        self.tics4 = gp.TicArray(self)
        self.tics5 = gp.TicArray(self)
        self.volume_ruler_top = gp.VolumeRuler(self, cache)
        self.volume_ruler_bottom1 = gp.VolumeRuler(self, cache)
        self.volume_ruler_bottom2 = gp.VolumeRuler(self, cache)
        self.date_ruler = gp.DateRuler(self, cache)
        self.icon_alerts1 = gp.IconAlert(self, cache)
        self.icon_alerts2 = gp.IconAlert(self, cache)
        self.icon_alerts3 = gp.IconAlert(self, cache)
        self.icon_alerts4 = gp.IconAlert(self, cache)
        self.macd1 = gp.MACD(self, cache)
        self.macd2 = gp.MACD(self, cache)
        self.flats1 = gp.BarChartH(self, cache)
        self.flats2 = gp.BarChartH(self, cache)
        self.chart_background = gp.Background(self, cache)

        # Widgets attached to parent (stuff attached to the master frame).

        self.statbar = StatBar(self.parent, self)
        self.ticker = gp.TickerTape(parent, cache)
        self.header_bar = tk.Frame(self.parent)
        self.footer_bar = tk.Frame(self.parent)
        self.lefthand_bar = tk.Frame(self.parent)
        self.righthand_bar = tk.Frame(self.parent)

    def configure_widgets(self, style: dict):
        """
        This will take our style and use it to set up all of our widgets.
        """
        if "WFI" not in self.labelvars.keys():
            self.labelvars.update({  # These are the static Wi-Fi and battery meters.
                'BAT': tk.IntVar(),
                'WFI': tk.IntVar()  # Remember these are being passed from OnScreen.update_variables
            })
        x, y = style['main']['price_canvas_offset_coord']
        self.place(x=x, y=y)
        # We need to pass our actual size because otherwise it won't be evident until after the first draw.
        width, height = int(style['main']['price_canvas_width']), int(style['main']['price_canvas_height'])
        self.style = style
        self.assets = list()
        inventory = self.__dict__.keys()
        for asset in style:
            if asset in inventory and asset in style['asset_order'] and asset in self.widgets:
                cmd = 'self.' + asset
                self.asset = eval(cmd)
                self.asset.canvas_width = width
                self.asset.canvas_height = height
                self.asset.configure(**style[asset])
                self.assets.append(eval(cmd))
        self.first = False
        return self

    def configure_actors(self):
        """
        Same as above but for the animated actors.
        """
        self.actors = list()
        inventory = self.__dict__.keys()
        for actor in self.style:
            if actor in inventory and actor in self.style['actor_order'] and actor in self.widgets:
                cmd = 'self.' + actor
                self.actor = eval(cmd)
                self.actor.build_content(
                    **self.style[actor]
                )
        return self

    def draw_widgets(self):
        """
        This will draw all the visual assets we have configured into
        """
        assets = self.style['asset_order']
        for asset in assets:
            exec('self.' + asset + '.draw()')
        return self

    def animate_actors(self):
        """
        animates our moving actors.
        """
        if not self.config['headless']:
            actors = self.style['actor_order']
            for actor in actors:
                exec('self.' + actor + '.animate()')
        return self

    def purge(self):
        """
        This will burn all the visual elements across all the widgets
        """
        for asset in self.assets:
            asset.burn_all()
        return self
