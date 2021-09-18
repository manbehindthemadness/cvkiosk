# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
This is out API client module allowing us to query information from the remote servers.
"""

import time
import numpy as np
from cvclient import Client
from utils import config, ticks_to_chart_time


class GetChart:
    """
    This will take the api based chart data and reformat it into something our legacy client can understand.

    Old format: Date,INDEX,MD500.Open,MD500.High,MD500.Low,MD500.Close,BTC.Open,BTC.High,BTC.Low,BTC.Close
    """
    def __init__(self):
        self.settings = config('settings')
        self.client = Client(self.settings['api_key'], self.settings['connection_string'])
        self.chart = None
        self.feed = None
        self.stamp = None
        self.dummy = None
        self.alerts = None

    def get_chart(self):
        """
        This will grab the chart data from the server and store it in our local CSV file.
        """
        s = self.settings
        self.chart = 'Date,INDEX,MD500.Open,MD500.High,MD500.Low,MD500.Close,BTC.Open,BTC.High,BTC.Low,BTC.Close\n'
        data = self.client.get_chart(
            chart_type=s['chart_type'],
            chart_length=s['chart_length'],
            chart_time=s['chart_time'],
            chart_focus=s['chart_focus'],
            chart_pair=s['chart_pair'],
            multiplier=s['chart_multiplier'],
            include_alerts='true'
        )
        if 'chart_data' in data.keys():
            feed_data = data['chart_data']
            price_data = data['price_data']
            alert_data = data['alert_data']
            pad_to = np.subtract(len(price_data), len(feed_data))
            if pad_to:
                padding = [feed_data[0]] * pad_to
                padding.extend(feed_data)
                feed_data = padding
            for bar in price_data:
                bar[0] = ticks_to_chart_time(bar[0])
            self.alerts, self.chart, self.feed = alert_data, price_data, feed_data
        else:
            print('unable to fetch chart data, retrying')
            time.sleep(5)
            self.get_chart()
        return self
