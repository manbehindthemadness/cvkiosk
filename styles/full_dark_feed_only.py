# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

"""


style = {
    'main': {  # The elements in the 'main' section must be defined for the style to parse.
        'style_name': 'full_dark',  # Name style for organization.
        # Configure global settings in relation to screen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_offset_coord': (0, 25),  # This is the coordinate of the upper left corner of the price canvas.
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:26-',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (75, 75, 35, 150),  # left, right, top, bottom.
        'price_increment': 6,  # The width of one candlestick in pixels.
        'background': 'black',
        'utc_format': '%H:%M:%p',
    },
    'indicators': {  # noqa
        'base': [
            {
                'overrides': {
                    'popt': {},
                    'fopt': {'macd': True}
                }
            }
        ],
        'on_balance_volume': [
            {'source': 'price'}
        ],
        'moving_average': [
            {'ema_spread': 9, 'source': 'feed'},
            {'ema_spread': 12, 'source': 'feed'},
            {'ema_spread': 26, 'source': 'feed'},
        ],
        'normal': [
            {'normal_base': 100, 'normal_spread': 1, 'source': 'feed'},
        ],
        'faema': [
            {'normal_base': 100, 'normal_spread': 1, 'ema_spread': 9},
            {'normal_base': 100, 'normal_spread': 1, 'ema_spread': 26},
        ],
        'faobv': [
            {'normal_spread': 1, 'obv_spread': 12, 'faobv_spread': 1},
        ],
        'directional_drift': [
            {'ema_spread': 1, 'source': 'feed', 'polarity': 'negative'},
            {'ema_spread': 1, 'source': 'feed', 'polarity': 'positive'},
        ],
        'normalized_directional_drift': [
            {'source': 'feed'},
        ],
        'variety': [
            {'ema_spread': 0},
        ],
        'triggers': [  # noqa
            {'type': 'updown', 'base': '_feed_normal_100_1', 'target': 'feed_ema_26', 'name': '_ema_26_trig'},
        ]
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'smoothi_bottom_backdrop',
        'smoothi_bottom',
        'smoothi_top',
        # 'candlesticks',
        'macd2',
        'macd1',
        'flats1',
        'price_ruler',
        'tics1',
        'date_ruler',
        'schematic',
        'tics2',
    ],
    'actor_order': [  # Animate order for moving actors.
        'statbar',
        'ticker'
    ],
    # From this point we wil divide this style into sections including the relational configuration respectively.
    'statbar': {
        'height': 25,
        'width': '$_screen_width:100%',
        'coords': (0, 0),  # Upper left-hand corner.
        'border': 0,
        'text_color': 'white',
        'meter_colors_left': "@gp.color_range(0, 100, 'red', 'green')",  # This is an eval statement, it can pass anything in utils.py
        'meter_colors_right': "@gp.color_range(0, 100, 'red', 'green')",
        'meter_label_width_left': 78,
        'meter_label_width_right': 78,
        'font': 'Arial 10 normal bold',
        'average': 3,   # This averages the readout across a few samples (useful for noisy sensors).
        'background': '#1a1c1c',
    },
    'candlesticks': {
        # The bar_width will alter the X coordinates of all the price related widgets.
        'geometry': '&_feed_price_matrix',
        'height': '$_screen_height:50%',
        'color1': '#2eff62',
        'color2': '#ff2e2e',
        'alpha': 0.75,
        'hollow': []  # ['red']  # This can hole one none or both of the colors.
    },
    'macd1': {
        'geometry': '&_feed_price_matrix',
        'offset': 457,
        'height': 400,
        'lineinterpol': 8,
        'lengths': [9, 12, 26],
        'x_shift': 6,
        'graph_type': 'prices',
        'kwargs': {
            '9': {
                'width': 1,
                'fill': 'purple',
                'smooth': 5,
                'rad': 2,
                'alpha': 0.8,
                'linetype': 'scatter'
            },
            '12': {
                'width': 1,
                'fill': 'violet',
                'smooth': 5,
                'rad': 2,
                'alpha': 0.8,
                'linetype': 'scatter'
            },
            '26': {
                'width': 2,
                'fill': 'deepskyblue',
                'rad': 2,
                'alpha': 0.8,
                'linetype': 'scatter'
            },
        }
    },
    'macd2': {
        'geometry': '&_feed_price_matrix',
        'offset': 457,
        'height': 600,
        'lineinterpol': 8,
        'lengths': [9, 12, 26],
        'x_shift': 6,
        # 'normalize': True,
        'kwargs': {
            '9': {
                'width': 1,
                'fill': 'black',
                'smooth': 5,
                'rad': 2,
                'alpha': 0.8,
                # 'linetype': 'scatter'
            },
            '12': {
                'width': 1,
                'fill': 'black',
                'smooth': 5,
                'rad': 2,
                'alpha': 0.8,
                # 'linetype': 'scatter'
            },
            '26': {
                'width': 2,
                'fill': 'black',
                'rad': 2,
                'alpha': 0.8,
                # 'linetype': 'scatter'
            },
        }
    },
    'flats1': {
        'geometry': '&_feed_price_matrix',
        'thickness': 3,
        'offset': 457,
        'bottom': 80,
        'height': 400,
        'alpha': 0.25,
        'outline': None,
        'grad': ('#1a1c1c', 'deepskyblue', 'v'),
        'grad1': ('#1a1c1c', 'deepskyblue', 'v'),
        'color': 'green',
        'color1': 'violet',
        'tb': 'c',
        'graph_type': 'volume',
        'smooth': 0
    },
    'smoothi_bottom': {
        'geometry': '&_feed_price_matrix',
        # 'matrix_override': '&_feed_normal_100_1',
        'height': 293,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'dodgerblue', 'v'),  # Gradient.
        'graph_type': 'volume',
        'tb': 'b',  # Top or bottom style.
        'outline': 'black',
        'smooth': 2,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 732,
        'padding': (75, 69, 0, 0),  # left, right, top, bottom.
        'alpha': 0.9,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_bottom_backdrop': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_feed_dd_1_positive',
        'height': 293,
        'fill': 'aqua',
        'grad': ('green', 'midnightblue', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'outline': 'black',
        'smooth': 3,  # Smooths average out the measurements.
        'lineinterpol': 4,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 717,
        'padding': (75, 69, 0, 21),  # left, right, top, bottom.
        'alpha': 0.1,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0),  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&feed_variety_0',
        'height': 135,
        'fill': 'dodgerblue',
        # 'grad': ('deepskyblue', 'dodgerblue', 'v'),  # Gradient.
        'graph_type': 'volume',
        'tb': 't',
        'smooth': 3,
        'lineinterpol': 4,
        'offset': 915,
        'padding': (69, 75, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.3,
        'aa': (10, 0),
    },
    'tics1': {  # These are the little ruler ticks that run down the edges.
        'coords': (1847, 0, 1847, 1027),  # top x, y, bottom x, y
        'tics': [3, 5, 9],  # shorts, longs, increment.
        'style': {
            'fill': '#adadad',
            'anchor': 'w',
            'width': 1,
        }
    },
    'price_ruler': {
        'geometry': '&_price_matrix',
        'coords': (1847, 0),
        'height': 1027,
        'width': 73,
        'price_range': '&_prices',
        'quotes': '',
        'style': {
            'font': 'Arial 10 normal bold',
            'linecolor': '#adadad',
            'linethickness': 1,
            'colorup': 'green',
            'colordown': 'red',
            'toptextcolor': 'white',
            'bottomtextcolor': 'white',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': None,
            'quoteheight': 7,
            'quoteoffset': -7,
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom.
            'anchor': 'ne',
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
    },
    'date_ruler': {
        'geometry': '&_price_matrix',
        'coords': (1847, 700),
        'time_coord': 75,
        'height': 50,
        'width': 73,
        'style': {
            'font': 'Arial 10 normal bold',
            'timequotefont': 'Arial 9 normal normal',
            'timequoteanchor': 'ne',
            'timeanchor': 'center',
            'timecolor': 'black',
            'timeruler_color': 'black',
            'timeformat': '%d.%I:%M%p',
            'dateformat': '%d.%I:%M%p',
            'timeoffset': -18,
            'linecolor': '#adadad',
            'timelinecolor': '#adadad',
            'markerstyle': 'default',
            'markersize': -10,
            'linethickness': 1,
            'outlinestyle': (0, 0, 0, 0),  # left, right, top, bottom (of the quote box).
            'timeoutlinestyle': (0, 0, 1, 0),  # left, right, top, bottom (of the date ruler).
            'timeoutline_extras': {'dash': (1, 1)},
            'quoteoffset': 6,
            'quotetextcolor': 'white',
            'anchor': 'e',
            'time_increment': 7,
            'use_local_time': False,
            'hide_info_text': True,
        },
    },
    'tics2': {  # These are the little ruler ticks that run down the edges.
        'coords': (78, 0, 79, 1027),  # top x, y, bottom x, y
        'tics': [3, 5, 9],  # shorts, longs, increment.
        'style': {
            'fill': '#adadad',
            'anchor': 'e',
            'width': 1,
        }
    },
    'schematic': {  # This is where all the fancy pointer lines go to show information.
        'geometry': '&_price_matrix',
        'coords': (0, 0),
        'width': 79,
        'height': 1027,
        'path_spacing': 20,  # This is how close the lines are allowed to get to one another.
        'path_relief': 15,  # Distance from the target pointer to the start of the line.
        'pointer_relief': -5,  # Distance between line end and the ruler.
        'font': 'Arial 10 normal normal',
        'linetype': 'line',  # More options to come in the future.
        'style': {
            'smooth': True,
            'dash': (1, 2),
            'arrow': 'last',
            'arrowshape': (5, 5, 2),
            'tag_fill': 'white',
            'outlinestyle': (0, 0, 1, 1),
            'linecolor': '#adadad',
            'linethickness': 1,
            'fill': '#3a3d3d',
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
    },
    'ticker': {
        'style': {
            'background': '#1a1c1c',
            'colorup': '#2eff62',
            'colordown': '#ff2e2e',
            'tickerfont': 'Arial 10 normal bold',
            'tickerfontcolorup': 'white',
            'tickerfontcolordown': 'white',
            'tickerbgup': '#1a1c1c',
            'tickerbgdown': '#1a1c1c',
            'quotefont': 'Arial 10 normal bold',
            'quotefontcolorup': '#2eff62',
            'quotebgdown': '#1a1c1c',
            'quotebgup': '#1a1c1c',
            'quotefontcolordown': '#ff2e2e',
            'iconup': None,
            'icondown': None,
            'symbolup': '▲',
            'symboldown': '▼',
            'symbolwidth': 8,
            'pix_per_step': 2,
            'step_delay': 50,
            'spacing': 1,
            'height': 25,
            'width': '$_screen_width:100%',
            'x': 0,
            'y': 1058
            },
        'clear': True,
        'content': '&_alerts',
        'content_type': 'alerts'
    }

}
