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
from utils import config
from graphiend import (
    utils,
    base,
    widgets,
    uxutils,
)


class Layout(base.Diagram):
    """
    This is the base layout class for the various user interface configurations.
    """
    style = dict()
    data = dict()

    def __init__(self, parent: tk.Frame, cache: utils.ImgCache, settings: config):
        """
        Basically we are going to init all the visual elements we plan to use here and just call them when needed.
        """
        base.Diagram.__init__(self, parent)
        self.parent = parent
        self.cache = cache
        self.config = settings
        self.assets = list()  # Visual assets
        self.actors = list()  # Active elements (moving).

        # Get widgets.

        self.pix = uxutils.ChartToPix
        self.sticks = widgets.CandleSticks(self, cache)
        self.smoothi_top = widgets.SmoothiVolumeH(self, cache)
        self.smoothi_bottom = widgets.SmoothiVolumeH(self, cache)
        self.schematic = widgets.SchematicRuler(self, cache)
        self.schematic_tics = widgets.TicArray(self)
        self.volume = widgets.SpikyVolumeH(self, cache)
        self.top_arrows = widgets.ArrowAlert(self, cache)
        self.bottom_arrows = widgets.ArrowAlert(self, cache)
        self.onions1 = widgets.OnionRingAlert(self, cache)
        self.icing_top = widgets.IcingAlert(self, cache)
        self.icing_bottomm = widgets.IcingAlert(self, cache)
        self.line_1 = widgets.Line(self, cache)
        self.line_2 = widgets.Line(self, cache)
        self.line_3 = widgets.Line(self, cache)
        self.price_ruler = widgets.PriceRuler(self, cache)
        self.price_tics = widgets.TicArray(self)
        self.volume_ruler_top = widgets.VolumeRuler(self, cache)
        self.volume_ruler_bottom = widgets.VolumeRuler(self, cache)
        self.date_ruler = widgets.DateRuler(self, cache)
        self.icon_alerts_1 = widgets.IconAlert(self, cache)
        self.icon_alerts_2 = widgets.IconAlert(self, cache)
        self.chart_background = widgets.Background(self, cache)

        # Widgets attached to parent (stuff attached to the master frame).

        self.ticker = widgets.TickerTape(parent, cache)
        self.header_bar = tk.Frame(self.parent)
        self.footer_bar = tk.Frame(self.parent)
        self.lefthand_bar = tk.Frame(self.parent)
        self.righthand_bar = tk.Frame(self.parent)

    def draw(self):
        """
        This will draw all the visual assets we have configured into
        :return:
        """
        for asset in self.assets:
            asset.draw()
        for actor in self.actors:
            actor.animate()
        return self

    def purge(self):
        """
        This will burn all the visual elements across all the widgets
        """
        for asset in self.assets:
            asset.burn()  # This is going to need some compat.
        return self
