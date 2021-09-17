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
"""
import tkinter as tk
import graphiend as gp
from utils import config


class Layout(gp.Diagram):
    """
    This is the base layout class for the various user interface configurations.
    """
    style = dict()
    data = dict()

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
        self.schematic = gp.SchematicRuler(self, cache)
        self.schematic_tics = gp.TicArray(self)
        self.volume = gp.SpikyVolumeH(self, cache)
        self.top_arrows = gp.ArrowAlert(self, cache)
        self.bottom_arrows = gp.ArrowAlert(self, cache)
        self.onions1 = gp.OnionRingAlert(self, cache)
        self.icing_top = gp.IcingAlert(self, cache)
        self.icing_bottomm = gp.IcingAlert(self, cache)
        self.line_1 = gp.Line(self, cache)
        self.line_2 = gp.Line(self, cache)
        self.line_3 = gp.Line(self, cache)
        self.price_ruler = gp.PriceRuler(self, cache)
        self.price_tics = gp.TicArray(self)
        self.volume_ruler_top = gp.VolumeRuler(self, cache)
        self.volume_ruler_bottom = gp.VolumeRuler(self, cache)
        self.date_ruler = gp.DateRuler(self, cache)
        self.icon_alerts_1 = gp.IconAlert(self, cache)
        self.icon_alerts_2 = gp.IconAlert(self, cache)
        self.chart_background = gp.Background(self, cache)

        # Widgets attached to parent (stuff attached to the master frame).

        self.ticker = gp.TickerTape(parent, cache)
        self.header_bar = tk.Frame(self.parent)
        self.footer_bar = tk.Frame(self.parent)
        self.lefthand_bar = tk.Frame(self.parent)
        self.righthand_bar = tk.Frame(self.parent)

    def configure_widgets(self, style: dict):
        """
        This will take our style and use it to set up all of our widgets.
        """
        # self.pack(expand=True, fill='both')  # Need to refresh the values.
        self.place(x=0, y=0)
        self.update()
        width, height = self.winfo_width(), self.winfo_height()
        self.style = style
        self.assets = list()  # TODO: We need to figure out how to keep the ordering intact...it's a dict...
        inventory = self.__dict__.keys()
        for asset in style:
            if asset in inventory and asset in style['asset_order']:
                cmd = 'self.' + asset
                print(cmd)
                self.asset = eval(cmd)
                self.asset.canvas_width = width
                self.asset.canvas_height = height
                self.asset.configure(**style[asset])
            elif asset in inventory and asset in style['actor_order']:
                actor = asset
                cmd = 'self.' + actor
                print(cmd)
                self.actor = eval(cmd)
                self.actor.build_content(
                    **style[actor]
                )

    def draw_widgets(self):
        """
        This will draw all the visual assets we have configured into
        """
        assets = self.style['asset_order']
        for asset in assets:
            exec('self.' + asset + '.draw()')
        actors = self.style['actor_order']
        for actor in actors:  # TODO: I don't think this is gonna work.
            exec('self.' + actor + '.animate()')

    def purge(self):
        """
        This will burn all the visual elements across all the widgets
        """
        for asset in self.assets:
            asset.burn()  # This is going to need some compat.
        return self
