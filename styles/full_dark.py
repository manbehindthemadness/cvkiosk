# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------

Remember to solve the chart size as an EVEN number of the screenwidth divided by price_increment plus the largest moving average.

(1920/6) + 100 = 420

"""


style = {  # REMEMBER TO USE THIS WITH A CHART LENGTH OF 420
    'main': {  # The elements in the 'main' section must be defined for the style to parse.
        'style_name': 'full_dark',  # Name style for organization.
        # Configure global settings in relation to screen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_offset_coord': (0, 25),  # This is the coordinate of the upper left corner of the price canvas.
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:26-',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (81, 75, 145, 150),  # left, right, top, bottom.
        'price_increment': 6,  # The width of one candlestick in pixels.
        'background': 'black',
        'utc_format': '%H:%M:%p',
    },
    'indicators': {  # noqa
        'down_swing': [
            {'source': 'feed', 'guides': (2, 50, 100)},
        ],
        'pure_faema': [
            {'normal_base': 101, 'normal_spread': 2, 'ema_spread': 10},
            {'normal_base': 101, 'normal_spread': 2, 'ema_spread': 25},
        ],
        'directional_drift': [
            {'ema_spread': 1, 'source': 'feed', 'polarity': 'negative'},
        ],
        'normalized_directional_drift': [
            {'source': 'feed', 'polarity': 'negative', 'normal_base': 101, 'normal_spread': 2, 'ema_spread': 10, }
        ],
        'triggers': [  # noqa
            {'type': 'updown', 'base': '_pure_faema_101_2_25', 'target': '_pure_faema_101_2_10', 'name': '_ema_9_trig'},
            {'type': 'hybrid_scale', 'averages': ['_feed_pure_normal_101_2', '_pure_faema_101_2_10'], 'lengths': (26, 25, 75), 'name': '_hi_mac'},  # Onions.
            {'type': 'crossup', 'base': '_hi_mac_1', 'target': '_hi_mac_2', 'name': '_hi_mac_up_trig', 'rad': 50},  # Onions.
            {'type': 'crossdown', 'base': '_hi_mac_1', 'target': '_hi_mac_2', 'name': '_hi_mac_down_trig', 'rad': 50},  # Onions.
            {'type': 'crossup', 'base': '_pure_faema_101_2_25', 'target': '_pure_faema_101_2_10', 'name': '_ema_9_point_trig_down'},
            {'type': 'crossdown', 'base': '_pure_faema_101_2_25', 'target': '_pure_faema_101_2_10', 'name': '_ema_9_point_trig_up'},
            {'type': 'cross_filter', 'crossup': '_ema_9_point_trig_up', 'crossdown': '_ema_9_point_trig_down', 'limit': 5, 'log_alerts': 1},
            {'type': 'updown', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_trig'},
            {'type': 'crossup', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_point_trig_up'},
            {'type': 'crossdown', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_point_trig_down'},
            {'type': 'cross_filter', 'crossup': '_ema_26_point_trig_up', 'crossdown': '_ema_26_point_trig_down', 'limit': 5, 'log_alerts': 1},
            {'type': 'trend', 'target': '_eno_feed_101_2_10_negative', 'name': '_eno_feed_trig'},
            {'type': 'point_trend', 'target': '_feed_dd_1_negative', 'name': '_feed_dd_1_negative_trig'},
        ]
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'shmacd',
        # 'smoothi_bottom_backdrop',
        # 'smoothi_bottom',
        'smoothi_top_backdrop_shadow',
        'smoothi_top_backdrop',
        'smoothi_top',
        'volume',
        'onions1',
        'onions2',
        'top_arrows',
        'top_arrows_invalid',
        'bottom_arrows',
        'bottom_arrows_invalid',
        'points1',
        'points1_invalid',
        'points2',
        'points2_invalid',
        'line1',
        'line2',
        # 'line3',
        # 'line4',
        'candlesticks',
        'icing_top1',
        'icing_top2',
        'icing_bottom1',
        'icing_bottom2',
        'volume_ruler_top',
        'volume_ruler_bottom1',
        'volume_ruler_bottom2',
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
        'coords': (0, 0),  # Upper left hand corner.
        'border': 0,
        'text_color': 'white',
        'meter_colors_left': "@gp.color_range(0, 100, 'red', 'green')",  # This is an eval statement, it can pass anything in utils.py
        'meter_colors_right': "@gp.color_range(0, 100, 'red', 'green')",
        'meter_label_width_left': 78,
        'meter_label_width_right': 78,
        'font': 'Arial 10 normal bold',
        'average': 3,   # This averages the readout across a few samples (useful for noisy sensors).
        'background': 'black',
    },
    'candlesticks': {
        # The bar_width will alter the X coordinates of all the price related widgets.
        'geometry': '&_price_matrix',
        'height': '$_screen_height:50%',
        'color1': '#2eff62',
        'color2': '#ff2e2e',
        'alpha': 0.75,
        'hollow': []  # ['red']  # This can hole one none or both of the colors.
    },
    'line1': {
        'matrix_override': '&_pure_faema_101_2_10',
        'geometry': '&_price_matrix',
        'smooth': 0,
        'width': 1,
        'color1': 'green',
        'color2': 'purple',
        'triggers': '&_ema_9_trig',
        'linetype': 'scatter',
        'lineinterpol': 2,
        'rad': 2,
        'alpha': 0.9
    },
    'line2': {
        'matrix_override': '&_pure_faema_101_2_25',
        'geometry': '&_price_matrix',
        'smooth': 0,
        'width': 1,
        'color1': 'magenta',
        'color2': 'lime',
        'triggers': '&_ema_26_trig',
        'linetype': 'scatter',
        'lineinterpol': 2,
        'rad': 2,
        'alpha': 0.5
    },
    'line3': {
        'matrix_override': '&_hi_mac_2',
        'geometry': '&_price_matrix',
        'smooth': 4,
        'width': 1,
        'color1': 'deepskyblue',
        'color2': 'violet',
        # 'triggers': '&_faobv_1_12_trig',
        'linetype': 'scatter',
        'lineinterpol': 2,
        'rad': 2,
        'alpha': 0.5
    },
    'line4': {
        'matrix_override': '&_hi_mac_1',
        'geometry': '&_price_matrix',
        'smooth': 4,
        'width': 1,
        'color1': 'yellow',
        'color2': 'yellow',
        # 'triggers': '&_ema_26_trig',
        'linetype': 'scatter',
        'lineinterpol': 2,
        'rad': 2,
        'alpha': 0.5
    },
    'shmacd': {  # noqa
        'geometry': '&_feed_price_matrix',
        'height': 110,
        'graph_type': 'prices',
        'tb': 'b',
        'smooth': 0,
        'lineinterpol': 2,
        'offset': 917,
        'padding': (75, 69, 0, 25),
        'aa': (10, 0),
        'lengths': (26, 25, 75),
        # 'extra': 100,
        'blend_1': '&_feed_pure_normal_101_2',
        'blend_2': '&_pure_faema_101_2_10',
        'kwargs': {
            '0': {
                'alphamask': False,
                'alpha': 0.7,
                'grad': ('violet', 'purple', 'v'),
                'outline': None,
                'fill': 'violet'
            },
            '1':
            {
                'alphamask': False,
                'alpha': 0.5,
                'grad': ('deepskyblue', 'blue', 'v'),
                'outline': None,
                'fill': 'deepskyblue'
            },
        }
    },
    'smoothi_bottom': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_feed_pure_normal_101_2',
        'height': 93,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'blue', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'smooth': 0,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 917,
        'padding': (75, 69, 0, 25),  # left, right, top, bottom.
        'alpha': 0.9,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_bottom_backdrop': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_pure_faema_101_2_10',
        'height': 93,
        'fill': 'aqua',
        'grad': ('violet', 'purple', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'outline': 'black',
        'smooth': 0,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 917,
        'padding': (75, 69, 0, 25),  # left, right, top, bottom.
        'alpha': 0.1,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_feed_dd_1_negative',
        'height': 135,
        'fill': '#ff2e2e',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 1,
        'lineinterpol': 4,
        'offset': 915,
        'padding': (69, 75, 0, 0),  # left, right, top, bottom.
        'alpha': 0.9,
        'aa': (10, 0),
    },
    'smoothi_top_backdrop': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_down_swing_feed_2_50_100',
        'height': 135,
        'fill': 'firebrick',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 3,
        'lineinterpol': 4,
        'offset': 915,
        'padding': (69, 75, 0, 0),  # left, right, top, bottom.
        'alpha': 0.5,
        'aa': (10, 0),
    },
    'smoothi_top_backdrop_shadow': {
        'geometry': '&_feed_price_matrix',
        'height': 135,
        'fill': 'dodgerblue',
        'graph_type': 'volume',
        'tb': 't',
        'smooth': 3,
        'lineinterpol': 4,
        'offset': 915,
        'padding': (69, 75, 0, 6),  # left, right, top, bottom.
        'alpha': 0.25,
        'aa': (10, 0),
    },
    'volume': {
        'geometry': '&_price_matrix',
        'height': 40,
        'top': 50,
        'bottom': 978,
        'offset': 935,
        'alpha': 0.9,
        'aa': (10, 0),
        'color1': '#2eff62',
        'color2': '#ff2e2e',
        'graph_type': 'volume',
        'tb': 'b'
    },
    'onions1': {
        'geometry': '&_price_matrix',
        'triggers': '&_hi_mac_up_trig',
        'color': 'yellow',
        'thickness': 2,
        'outline': 'gold',
        'alpha': 0.2,
        'aa': (10, 1),
        'multiplier': 1,
        'cutoff': 30,
        'tb': 'c',
        'use_schematic': False
    },
    'onions2': {
        'geometry': '&_price_matrix',
        'triggers': '&_hi_mac_down_trig',
        'color': 'blue',
        'thickness': 2,
        'outline': 'steelblue',
        'alpha': 0.35,
        'aa': (10, 1),
        'multiplier': 1,
        'cutoff': 30,
        'tb': 'c',
        'use_schematic': False
    },
    'top_arrows': {
        'geometry': '&_price_matrix',
        'height': 25,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'magenta',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that the arrow will attach.
        'arrowshape': (7, 7, 4),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cu',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_down',
        'tb': 't',
        'signal': 'TR.DN',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'white',  # Icon color.
        'tag_fill': 'white',  # Schematic text color.
        'use_schematic': True  # Toggle schematics.
    },
    'top_arrows_invalid': {
        'geometry': '&_price_matrix',
        'height': 25,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': '#380136',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that the arrow will attach.
        'arrowshape': (7, 7, 4),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cu',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_down_invalid',
        'tb': 't',
        'signal': 'TR.DN',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'white',  # Icon color.
        'tag_fill': 'white',  # Schematic text color.
        'use_schematic': False  # Toggle schematics.
    },
    'bottom_arrows': {
        'geometry': '&_price_matrix',
        'height': 25,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'cyan',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that the arrow will attach.
        'arrowshape': (7, 7, 4),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cl',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_up',
        'tb': 'b',
        'signal': 'TR.UP',
        'icon': 'img/icons/x1.png',  # Schematic view icon.
        'icon_fill': 'white',  # Icon color.
        'tag_fill': 'white',  # Schematic text color.
        'use_schematic': True  # Toggle schematics.
    },
    'bottom_arrows_invalid': {
        'geometry': '&_price_matrix',
        'height': 25,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': '#013836',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that the arrow will attach.
        'arrowshape': (7, 7, 4),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cl',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_up_invalid',
        'tb': 'b',
        'signal': 'TR.UP',
        'icon': 'img/icons/x1.png',  # Schematic view icon.
        'icon_fill': 'white',  # Icon color.
        'tag_fill': 'white',  # Schematic text color.
        'use_schematic': False  # Toggle schematics.
    },
    'points1': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_down',
        'color': 'magenta',
        'rad': 4,
        'alpha': 1.0,
        'offset': 25,
        'tb': 't',
        'direction': 'up',
        'icon': 'img/icons/minus.png',
        'icon_fill': 'white',
        'tag_fill': 'white',
        'signal': 'MT.DN',
        'use_schematic': True
    },
    'points1_invalid': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_down_invalid',
        'color': '#380136',
        'rad': 4,
        'alpha': 0.9,
        'offset': 25,
        'tb': 't',
        'direction': 'up',
        'icon': 'img/icons/minus.png',
        'icon_fill': 'white',
        'tag_fill': 'white',
        'signal': 'MT.DN',
        'use_schematic': False
    },
    'points2': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_up',
        'color': 'cyan',
        'rad': 4,
        'alpha': 1.0,
        'offset': 25,
        'tb': 'b',
        'direction': 'down',
        'icon': 'img/icons/minus.png',
        'icon_fill': 'white',
        'tag_fill': 'white',
        'signal': 'MT.UP',
        'use_schematic': True
    },
    'points2_invalid': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_up_invalid',
        'color': '#013836',
        'rad': 4,
        'alpha': 0.9,
        'offset': 25,
        'tb': 'b',
        'direction': 'down',
        'icon': 'img/icons/minus.png',
        'icon_fill': 'white',
        'tag_fill': 'white',
        'signal': 'MT.UP',
        'use_schematic': False
    },
    'icing_top1': {
        'geometry': '&_price_matrix',
        'triggers': '&_down_swing_feed_2_50_100_trig',
        'thickness': 1,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': '#ededed',
        'color2': '#dbdbdb',
        'tb': 't'
    },
    'icing_top2': {
        'geometry': '&_price_matrix',
        'triggers': '&_feed_dd_1_negative_trig',
        'thickness': 2,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'white',
        'color2': 'white',
        'tb': 't'
    },
    'icing_bottom1': {
        'geometry': '&_price_matrix',
        'triggers': '&_down_swing_feed_2_50_100_trig',
        'thickness': 1,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': '#ededed',
        'color2': '#dbdbdb',
        'tb': 'b'
    },
    'icing_bottom2': {
        'geometry': '&_price_matrix',
        'triggers': '&_feed_dd_1_negative_trig',
        'thickness': 2,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'white',
        'color2': 'white',
        'tb': 'b'
    },
    'tics1': {  # These are the little ruler ticks that run down the edges.
        'coords': (1847, 35, 1847, 905),  # top x, y, bottom x, y
        'tics': [3, 5, 9],  # shorts, longs, increment.
        'style': {
            'fill': '#adadad',
            'anchor': 'w',
            'width': 1,
        }
    },
    'volume_ruler_top': {
        'geometry': '&_price_matrix',
        'coords': (1847, 0),
        'height': 35,
        'width': 73,
        'price_range': '&_volume',
        'quotes': '&_drf',
        'style': {
            'font': 'Arial 10 normal normal',
            'linecolor': '#adadad',
            'linethickness': 1,
            'toptextcolor': '#adadad',
            'bottomtextcolor': '#adadad',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'white',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom.
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
    },
    'volume_ruler_bottom1': {
        'geometry': '&_price_matrix',
        'coords': (1847, 955),
        'height': 32,
        'width': 73,
        'price_range': '&_volume',
        'quotes': '&_drf',
        'style': {
            'font': 'Arial 10 normal normal',
            'linecolor': '#adadad',
            'linethickness': 1,
            'toptextcolor': 'white',
            'bottomtextcolor': 'white',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'white',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 0, 0),  # left, right, top, bottom.
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
    },
    'volume_ruler_bottom2': {
        'geometry': '&_price_matrix',
        'coords': (1847, 987),
        'height': 40,
        'width': 73,
        'price_range': '&_volume',
        'quotes': '&_volume_quote',
        'style': {
            'font': 'Arial 10 normal normal',
            'linecolor': '#adadad',
            'linethickness': 1,
            'toptextcolor': 'white',
            'bottomtextcolor': 'white',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'white',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom.
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
    },
    'price_ruler': {
        'geometry': '&_price_matrix',
        'coords': (1847, 35),
        'height': 870,
        'width': 73,
        'price_range': '&_prices',
        'quotes': '&_price_quote',
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
            'showquotepointer': True,
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
        'coords': (1847, 905),
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
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom (of the quote box).
            'timeoutlinestyle': (0, 0, 1, 0),  # left, right, top, bottom (of the date ruler).
            'timeoutline_extras': {'dash': (1, 1)},
            'quoteoffset': 6,
            'quotetextcolor': 'white',
            'anchor': 'e',
            'time_increment': 7,
            'use_local_time': True,
            'hide_info_text': False,
        },
        'background': {
            'fill': '#262929',
            'alpha': 0.5
        }
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
            'background': 'black',
            'colorup': '#2eff62',
            'colordown': '#ff2e2e',
            'tickerfont': 'Arial 10 normal bold',
            'tickerfontcolorup': 'white',
            'tickerfontcolordown': 'white',
            'tickerbgup': 'black',
            'tickerbgdown': 'black',
            'quotefont': 'Arial 10 normal bold',
            'quotefontcolorup': '#2eff62',
            'quotebgdown': 'black',
            'quotebgup': 'black',
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
