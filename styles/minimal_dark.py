# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

"""


style = {  # REMEMBER TO USE THIS WITH A CHART LENGTH OF 181
    'main': {  # The elements in the 'main' section must be defined for the style to parse.
        'style_name': 'tutorial',  # Name style for organization.
        # Configure global settings in relation to screen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_offset_coord': (0, 10),  # This is the coordinate of the upper left corner of the price canvas.
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:26-',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (2, 2, 35, 85),  # left, right, top, bottom.
        'price_increment': 4,  # The width of one candlestick in pixels.
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
            {'type': 'crossup', 'base': '_pure_faema_101_2_25', 'target': '_pure_faema_101_2_10', 'name': '_ema_9_point_trig_down'},
            {'type': 'crossdown', 'base': '_pure_faema_101_2_25', 'target': '_pure_faema_101_2_10', 'name': '_ema_9_point_trig_up'},
            {'type': 'cross_filter', 'crossup': '_ema_9_point_trig_up', 'crossdown': '_ema_9_point_trig_down', 'limit': 10},
            {'type': 'updown', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_trig'},
            {'type': 'crossup', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_point_trig_up'},
            {'type': 'crossdown', 'base': '_ac', 'target': '_pure_faema_101_2_25', 'name': '_ema_26_point_trig_down'},
            {'type': 'cross_filter', 'crossup': '_ema_26_point_trig_up', 'crossdown': '_ema_26_point_trig_down', 'limit': 10},
            {'type': 'trend', 'target': '_eno_feed_101_2_10_negative', 'name': '_eno_feed_trig'},
            {'type': 'point_trend', 'target': '_feed_dd_1_negative', 'name': '_feed_dd_1_negative_trig'},
        ]
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'smoothi_bottom_backdrop',
        'smoothi_bottom',
        'smoothi_top_backdrop',
        'smoothi_top',
        'volume',
        'top_arrows',
        'top_arrows_invalid',
        'bottom_arrows',
        'bottom_arrows_invalid',
        'points1',
        'points2',
        'line1',
        'line2',
        # 'line3',
        'candlesticks',
        'icing_top1',
        'icing_top2',
        'icing_bottom1',
        'icing_bottom2',
        'tics1',
        'date_ruler',
        'tics2',
    ],
    'actor_order': [  # Animate order for moving actors.
        'statbar',
        'ticker'
    ],
    # From this point we wil divide this style into sections including the relational configuration respectively.
    'statbar': {
        'height': 10,
        'width': '$_screen_width:100%',
        'coords': (0, 0),  # Upper left hand corner.
        'border': 0,
        'text_color': 'white',
        'meter_colors_left': "@gp.color_range(0, 100, 'red', 'green')",  # This is an eval statement, it can pass anything in utils.py
        'meter_colors_right': "@gp.color_range(0, 100, 'red', 'green')",
        'meter_label_width_left': 40,
        'meter_label_width_right': 40,
        'font': 'Arial 5 normal bold',
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
        'alpha': 0.5
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
    # 'line3': {
    #     'matrix_override': '&_faobv_1_12',
    #     'geometry': '&_price_matrix',
    #     'smooth': 4,
    #     'width': 1,
    #     'color1': 'deepskyblue',
    #     'color2': 'violet',
    #     'triggers': '&_faobv_1_12_trig',
    #     'linetype': 'scatter',
    #     'lineinterpol': 2,
    #     'rad': 2,
    #     'alpha': 0.5
    # },
    'smoothi_bottom': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_feed_pure_normal_101_2',
        'height': 60,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'blue', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'outline': 'black',
        'smooth': 4,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 150,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        'alpha': 0.2,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_bottom_backdrop': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_pure_faema_101_2_10',
        'height': 60,
        'fill': 'aqua',
        'grad': ('violet', 'purple', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        # 'outline': 'black',
        'smooth': 4,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 150,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        'alpha': 0.1,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_feed_dd_1_negative',
        'height': 20,
        'fill': '#ff2e2e',
        'graph_type': 'prices',
        'tb': 't',
        'outline': 'black',
        'smooth': 2,
        'lineinterpol': 4,
        'offset': 192,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.8,
        'aa': (10, 0),
    },
    'smoothi_top_backdrop': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_down_swing_feed_2_50_100',
        'height': 20,
        'fill': '#ff2e2e',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 2,
        'lineinterpol': 4,
        'offset': 194,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.4,
        'aa': (10, 0),
    },
    'volume': {
        'geometry': '&_price_matrix',
        'height': 40,
        'top': 100,
        'bottom': 140,
        'offset': 70,
        'alpha': 0.6,
        'aa': (10, 0),
        'color1': '#2eff62',
        'color2': '#ff2e2e',
        'graph_type': 'volume',
        'tb': 'b'
    },
    'top_arrows': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'magenta',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
        'arrowshape': (4, 4, 1),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cu',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_down',
        'tb': 't',
        'signal': 'TR.DN',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'green',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': True  # Toggle schematics.
    },
    'top_arrows_invalid': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': '#380136',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
        'arrowshape': (4, 4, 1),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cu',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_down_invalid',
        'tb': 't',
        'signal': 'TR.DN',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'green',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': False  # Toggle schematics.
    },
    'bottom_arrows': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'cyan',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
        'arrowshape': (5, 5, 2),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cl',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_up',
        'tb': 'b',
        'signal': 'TR.UP',
        'icon': 'img/icons/x1.png',  # Schematic view icon.
        'icon_fill': 'red',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': True  # Toggle schematics.
    },
    'bottom_arrows_invalid': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': '#013836',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
        'arrowshape': (5, 5, 2),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_cl',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_ema_26_point_trig_up',
        'tb': 'b',
        'signal': 'TR.UP',
        'icon': 'img/icons/x1.png',  # Schematic view icon.
        'icon_fill': 'red',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': False  # Toggle schematics.
    },
    'points1': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_down',
        'color': 'magenta',
        'rad': 3,
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
        'rad': 3,
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
        'coords': (319, 0, 319, 140),  # top x, y, bottom x, y
        'tics': [1, 2, 9],  # shorts, longs, increment.
        'style': {
            'fill': '#adadad',
            'anchor': 'e',
            'width': 1,
        }
    },
    'date_ruler': {
        'geometry': '&_price_matrix',
        'coords': (320, 140),
        'time_coord': 2,
        'height': 50,
        'width': 50,
        'style': {
            'font': 'Arial 10 italic bold',
            'timequotefont': 'Arial 6 italic bold',
            'timequoteanchor': 'ne',
            'timeanchor': 'center',
            'timecolor': 'black',
            'timeruler_color': 'black',
            'timeformat': '%d.%I:%M%p',
            'dateformat': '%d.%I:%M%p',
            'timeoffset': 5,
            'linecolor': '#adadad',
            'timelinecolor': '#adadad',
            'markerstyle': 'default',
            'markersize': 10,
            'linethickness': 1,
            'outlinestyle': (1, 1, 1, 1),  # left, right, top, bottom (of the quote box).
            'timeoutlinestyle': (0, 0, 1, 0),  # left, right, top, bottom (of the date ruler).
            'timeoutline_extras': {'dash': (1, 1)},
            'quoteoffset': 6,
            'quotetextcolor': 'black',
            'anchor': 'e',
            'time_increment': 3,
            'use_local_time': True,
            'hide_info_text': True,
        },
        'background': {
            'fill': 'black',
            'alpha': 0.1
        }
    },
    'tics2': {  # These are the little ruler ticks that run down the edges.
        'coords': (0, 10, 0, 140),  # top x, y, bottom x, y
        'tics': [1, 2, 9],  # shorts, longs, increment.
        'style': {
            'fill': '#adadad',
            'anchor': 'w',
            'width': 1,
        }
    },
    'ticker': {
        'style': {
            'background': 'black',
            'colorup': '#2eff62',
            'colordown': '#ff2e2e',
            'tickerfont': 'Arial 6 normal bold',
            'tickerfontcolorup': 'white',
            'tickerfontcolordown': 'white',
            'tickerbgup': 'black',
            'tickerbgdown': 'black',
            'quotefont': 'Arial 6 normal bold',
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
            'height': 6,
            'width': '$_screen_width:100%',
            'x': 0,
            'y': 224
            },
        'clear': True,
        'content': '&_alerts',
        'content_type': 'alerts'
    }

}
