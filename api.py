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
from utils import config


price_cache = dict()  # This will cache our full-price history.
cursor = list()  # This will cache our second-to-last price, so we will know when to increment.


class GetChart:
    """
    This will take the api based chart data and reformat it into something our legacy client can understand.

    Old format: Date,INDEX,MD500.Open,MD500.High,MD500.Low,MD500.Close,BTC.Open,BTC.High,BTC.Low,BTC.Close
    """
    resample = True

    def __init__(self):
        global price_cache
        global cursor

        self.cache = price_cache
        self.cursor = cursor

        self.settings = config('settings')
        self.length = self.settings['chart_length']
        self.client = Client(self.settings['api_key'], self.settings['connection_string'])
        self.chart = None
        self.feed = None
        self.stamp = None
        self.dummy = None
        self.alerts = None
        self.variety = None

    def get_chart(self):
        """
        This will grab the chart data from the server and store it in our local CSV file.
        """
        s = self.settings
        kwargs = {
            'chart_type': s['chart_type'],
            'chart_length': self.length,
            'chart_time': s['chart_time'],
            'chart_focus': s['chart_focus'],
            'chart_pair': s['chart_pair'],
            'multiplier': s['chart_multiplier'],
            'include_variety': str(s['chart_variety']).lower(),
            'include_alerts': 'true'
        }
        self.chart = 'Date,INDEX,MD500.Open,MD500.High,MD500.Low,MD500.Close,BTC.Open,BTC.High,BTC.Low,BTC.Close\n'
        data = self.client.get_chart(**kwargs)
        if 'chart_data' in data.keys():
            # ----------------------------------------------------------------------------------------------------------
            # TODO: If this works well it should be moved into the CVClient package.
            if self.resample:  # Populate caches.
                self.cache = data
                self.cursor = data['price_data'][-2:]
            else:  # Update caches.
                """
                So what we are doing here is normalizing the time offset between the feed and price-action. We do this by 
                comparing the second to last price bar with the last update, when this changes we know it's time to 
                increment to the next sample.
                """
                updates = ['chart_data', 'price_data']
                if s['chart_variety']:
                    updates.append('variety_data')
                if self.cursor[0] == data['price_data'][-2]:  # We are on the same bar, so we just update the latest cached quotes.
                    # print('updating sample')
                    for update in updates:
                        self.cache[update][-1] = data[update][-1]
                else:  # The price bar has incremented, now we should append 1 sample and update the second to last cached.
                    self.cursor = data['price_data'][-2:]  # Update cursor.
                    for update in updates:
                        self.cache[update][-1] = data[update][-2]
                        self.cache[update].append(data[update][-1])
                        del self.cache[update][0]  # Trim length so we don't leak memory.
                self.cache['alert_data'] = data['alert_data']
            # ----------------------------------------------------------------------------------------------------------
            feed_data = self.cache['chart_data']
            price_data = self.cache['price_data']
            alert_data = self.cache['alert_data']
            variety_data = self.cache['variety_data']
            pad_to = np.subtract(len(price_data), len(feed_data))
            if pad_to:
                padding = [feed_data[0]] * pad_to
                padding.extend(feed_data)
                feed_data = padding
            self.variety, self.alerts, self.chart, self.feed = variety_data, alert_data, price_data, feed_data
            self.resample = False
            self.length = '2'
        else:
            print('unable to fetch chart data, retrying')
            time.sleep(5)
            self.get_chart()
        return self
