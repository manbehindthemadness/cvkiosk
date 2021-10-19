# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

This is our tutorial style,

Its important to note that some of these values are in markup and will be translated when the style is read into
    the logic. For example when a field valur starts with a doller sign '$_screen_width:100%' it will be evaluated
    based on the statement following the colon,
in this instance we will get a calculated value of 100% of the screen width. The underscore tells us that the value
    we are calculating against is outside of the style, alternatively we are able to calculate against other fields in
    the style as such: '$price_canvas_height:50%'. This will give us a calculated value of half of whatever the
    field 'price_canvas_height' contains. These statements can be chained to access subkeys as well:
    '$main$price_canvas_height:25%'.
    (EXPERIMENTAL: an @ at the beginning will cause the expression to be evaluated as a literal.)

Be aware that many of the naming conventions for the various parameters here are defined by third party logic and
    a result of this there is no standard naming convention. This will be corrected in a future build.

**IMPORTANT**: In order for a widget to be drawn on screen it needs to have the following:
                1. A style entry matching it's name.
                2. An entry in either asset_order or actor_order.
                3. an entry in the layouts.widgets array.

EXAMPLE:
    NOTE: Provide example...

"""
# NOTE: The constants are held in an alternate location by screen properties, these are only here for easy reference.
constants = {  # This is an example of the constants dictionary (not the one we actually use ;).
    '_screen_size': '500x400',
    '_screen_height': 400,
    '_screen_width': 500,
}

style = {
    'main': {  # The elements in the 'main' section must be defined for the style to parse.
        'style_name': 'tutorial',  # Name style for organization.
        # Configure global settings in relation to screen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_offset_coord': (0, 25),  # This is the coordinate of the upper left cornet of the price canvas.
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:50-',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (47, 46, 35, 155),  # left, right, top, bottom.
        'price_increment': 6,  # The width of one candlestick in pixels.
        'background': 'white',
        'utc_format': '%H:%M:%p',
    },
    'indicators': {  # noqa
        'moving_average': [
            {'ema_spread': 9, 'source': 'price'},
        ],
        'normal': [
            {'normal_base': 100, 'normal_spread': 1, 'source': 'feed'},
        ],
        'faema': [
            {'normal_base': 100, 'normal_spread': 1, 'ema_spread': 9},
            {'normal_base': 100, 'normal_spread': 1, 'ema_spread': 26},
        ],
        'directional_drift': [
            {'ema_spread': 1, 'source': 'feed', 'polarity': 'negative'},
        ],
        'normalized_directional_drift': [
            {'source': 'feed'},
        ],
        'triggers': [  # noqa
            {'type': 'updown', 'base': '_faema_100_1_26', 'target': '_faema_100_1_9', 'name': '_ema_9_trig'},
            {'type': 'crossup', 'base': '_faema_100_1_26', 'target': '_faema_100_1_9', 'name': '_ema_9_point_trig_down'},
            {'type': 'crossdown', 'base': '_faema_100_1_26', 'target': '_faema_100_1_9', 'name': '_ema_9_point_trig_up'},
            {'type': 'cross_filter', 'crossup': '_ema_9_point_trig_up', 'crossdown': '_ema_9_point_trig_down', 'limit': 10},
            {'type': 'updown', 'base': '_ac', 'target': '_faema_100_1_26', 'name': '_ema_26_trig'},
            {'type': 'crossup', 'base': '_ac', 'target': '_faema_100_1_26', 'name': '_ema_26_point_trig_up'},
            {'type': 'crossdown', 'base': '_ac', 'target': '_faema_100_1_26', 'name': '_ema_26_point_trig_down'},
            {'type': 'cross_filter', 'crossup': '_ema_26_point_trig_up', 'crossdown': '_ema_26_point_trig_down', 'limit': 10},
            {'type': 'trend', 'target': '_eno_feed', 'name': '_eno_feed_trig'},
            {'type': 'point_trend', 'target': '_feed_dd_1_negative', 'point': 304.0, 'name': '_feed_dd_1_negative_trig'},
        ],
        'audio_alerts': [  # These trigger audio alerts on the systems that include a speaker.
            {'source': '_ema_26_point_trig_down', 'alert_type': 'high_med_low', 'repeat': False},
            {'source': '_ema_26_point_trig_up', 'alert_type': 'low_med_high', 'repeat': False},
            {'source': '_ema_9_point_trig_down', 'alert_type': 'single_low', 'repeat': False},
            {'source': '_ema_9_point_trig_up', 'alert_type': 'single_high', 'repeat': False},
        ]
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'smoothi_bottom_backdrop',
        'smoothi_bottom',
        'smoothi_top_backdrop',
        'smoothi_top',
        'volume',
        'top_arrows',
        'bottom_arrows',
        'points1',
        'points2',
        'line1',
        'line2',
        'candlesticks',
        'icing_top1',
        'icing_top2',
        'icing_bottom1',
        'icing_bottom2',
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
        'coords': (0, 0),  # Uppr left hand corner.
        'border': 0,
        'text_color': 'black',
        'meter_colors_left': "@gp.color_range(0, 100, 'red', 'green')",  # This is an eval statement, it can pass anything in utils.py
        'meter_colors_right': "@gp.color_range(0, 100, 'red', 'green')",
        'meter_label_width_left': 50,
        'meter_label_width_right': 50,
        'font': 'Arial 9 normal bold',
        'average': 3,   # This averages the readout across a few samples (useful for noisy sensors).
        'background': 'white',
    },
    'candlesticks': {
        # The bar_width will alter the X coordinates of all the price related widgets.
        'geometry': '&_price_matrix',
        'height': '$_screen_height:50%',
        'color1': 'green',
        'color2': 'red',
        'alpha': 0.75,
        'hollow': []  # ['red']  # This can hole one none or both of the colors.
    },
    'line1': {
        'matrix_override': '&_faema_100_1_9',
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
        'matrix_override': '&_faema_100_1_26',
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
    'smoothi_bottom': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_normal_100_1',
        'height': 75,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'black', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'outline': 'white',
        'smooth': 1,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 250,
        'padding': (46, 46, 0, 0),  # left, right, top, bottom.
        'alpha': 0.2,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_bottom_backdrop': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_faema_100_1_9',
        'height': 75,
        'fill': 'aqua',
        'grad': ('violet', 'purple', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        # 'outline': 'black',
        'smooth': 1,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 250,
        'padding': (46, 46, 0, 0),  # left, right, top, bottom.
        'alpha': 0.1,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_feed_dd_1_negative',
        'height': 30,
        'fill': 'red',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 2,
        'lineinterpol': 4,
        'offset': 320,
        'padding': (46, 46, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.7,
        'aa': (10, 0),
    },
    'smoothi_top_backdrop': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_eno_feed',
        'height': 30,
        'fill': '#ff2e2e',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 2,
        'lineinterpol': 4,
        'offset': 320,
        'padding': (46, 46, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.4,
        'aa': (10, 0),
    },
    'volume': {
        'geometry': '&_price_matrix',
        'height': 75,
        'top': 200,
        'bottom': 200,
        'offset': 75,
        'alpha': 0.7,
        'aa': (10, 0),
        'color1': 'green',
        'color2': 'red',
        'graph_type': 'volume',
        'tb': 'b'
    },
    'top_arrows': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'blueviolet',
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
    'bottom_arrows': {
        'geometry': '&_price_matrix',
        'height': 10,
        'offset': 10,  # This is the distance the arrow will appear from the coordinate.
        'fill': 'magenta',
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
    # 'onions1': {
    #     'geometry': '&_price_matrix',
    #     'matrix_override': '&_ac',
    #     'triggers': '&_triggers3',
    #     'color': 'cyan',
    #     'thickness': 2,
    #     'outline': 'steelblue',
    #     'alpha': 0.6,
    #     'aa': (10, 1),
    #     'multiplier': 2,  # This is the multiplication of the radius versus the trigger value.
    #     'cutoff': 20,  # This is the maximum size limit.
    #     'tb': 'c',  # Center objects.
    #     'icon': 'img/icons/heavy_circle.png',
    #     'icon_fill': 'steelblue',
    #     'tag_fill': 'black',
    #     'signal': 'M',
    #     'use_schematic': True
    # },
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
        'use_schematic': True
    },
    'points2': {
        'geometry': '&_price_matrix',
        'triggers': '&_ema_9_point_trig_up',
        'color': 'blue',
        'rad': 3,
        'alpha': 0.9,
        'offset': 25,
        'tb': 'b',
        'direction': 'down',
        'icon': 'img/icons/minus.png',
        'icon_fill': 'white',
        'tag_fill': 'white',
        'signal': 'MT.UP',
        'use_schematic': True
    },
    'icing_top1': {
        'geometry': '&_price_matrix',
        'triggers': '&_eno_feed_trig',
        'thickness': 1,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': '#262626',
        'color2': '#262626',
        'tb': 't'
    },
    'icing_top2': {
        'geometry': '&_price_matrix',
        'triggers': '&_feed_dd_1_negative_trig',
        'thickness': 2,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'black',
        'color2': 'black',
        'tb': 't'
    },
    'icing_bottom1': {
        'geometry': '&_price_matrix',
        'triggers': '&_eno_feed_trig',
        'thickness': 1,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': '#262626',
        'color2': '#262626',
        'tb': 'b'
    },
    'icing_bottom2': {
        'geometry': '&_price_matrix',
        'triggers': '&_feed_dd_1_negative_trig',
        'thickness': 2,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'black',
        'color2': 'black',
        'tb': 'b'
    },
    'volume_ruler_top': {
        'geometry': '&_price_matrix',
        'coords': (450, 0),
        'height': 35,
        'width': 50,
        'price_range': '&_volume',
        'quotes': '&_volume_quote',
        'style': {
            'font': 'Arial 7 normal normal',
            'linecolor': 'grey',
            'linethickness': 1,
            'toptextcolor': 'grey',
            'bottomtextcolor': 'grey',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'grey',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom.
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'volume_ruler_bottom1': {
        'geometry': '&_price_matrix',
        'coords': (450, 250),
        'height': 50,
        'width': 50,
        'price_range': '&_volume',
        'quotes': '&_volume_quote',
        'style': {
            'font': 'Arial 7 normal normal',
            'linecolor': 'grey',
            'linethickness': 1,
            'toptextcolor': 'grey',
            'bottomtextcolor': 'grey',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'grey',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 1, 0),  # left, right, top, bottom.
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'volume_ruler_bottom2': {
        'geometry': '&_price_matrix',
        'coords': (450, 300),
        'height': 48,
        'width': 50,
        'price_range': '&_volume',
        'quotes': '&_volume_quote',
        'style': {
            'font': 'Arial 7 normal normal',
            'linecolor': 'grey',
            'linethickness': 1,
            'toptextcolor': 'grey',
            'bottomtextcolor': 'grey',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': False,
            'quotetextcolor': 'grey',
            'quoteheight': 6,
            'quoteoffset': 3,
            'outlinestyle': (0, 0, 1, 1),  # left, right, top, bottom.
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'tics1': {  # These are the little ruler ticks that run down the edges.
        'coords': (452, 35, 452, 190),  # top x, y, bottom x, y
        'tics': [2, 4, 9],  # shorts, longs, increment.
        'style': {
            'fill': 'grey',
            'anchor': 'w',
            'width': 1,
        }
    },
    'price_ruler': {
        'geometry': '&_price_matrix',
        'coords': (450, 35),
        'height': 160,
        'width': 50,
        'price_range': '&_prices',
        'quotes': '&_price_quote',
        'style': {
            'font': 'Arial 7 normal bold',
            'linecolor': 'grey',
            'linethickness': 1,
            'colorup': 'green',
            'colordown': 'red',
            'toptextcolor': 'grey',
            'bottomtextcolor': 'grey',
            'topbottomtextoffsets': (1, 5),
            'showtopbottomquotes': False,
            'showquotepointer': True,
            'quotetextcolor': None,
            'quoteheight': 7,
            'quoteoffset': -7,
            'outlinestyle': (0, 0, 0, 1),  # left, right, top, bottom.
            'anchor': 'ne',
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'date_ruler': {
        'geometry': '&_price_matrix',
        'coords': (450, 195),
        'time_coord': 50,
        'height': 50,
        'width': 50,
        'style': {
            'font': 'Arial 10 italic bold',
            'timequotefont': 'Arial 6 italic bold',
            'timequoteanchor': 'ne',
            'timeanchor': 'center',
            'timecolor': 'grey',
            'timeruler_color': 'grey',
            'timeformat': '%d.%I:%M%p',
            'dateformat': '%d.%I:%M%p',
            'timeoffset': 5,
            'linecolor': 'grey',
            'timelinecolor': 'grey',
            'markerstyle': 'default',
            'markersize': 10,
            'linethickness': 1,
            'outlinestyle': (0, 0, 0, 0),  # left, right, top, bottom (of the quote box).
            'timeoutlinestyle': (0, 0, 1, 0),  # left, right, top, bottom (of the date ruler).
            'timeoutline_extras': {'dash': (1, 1)},
            'quoteoffset': 6,
            'quotetextcolor': 'grey',
            'anchor': 'e',
            'time_increment': 5,
            'use_local_time': True,
            'hide_info_text': False,
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'tics2': {  # These are the little ruler ticks that run down the edges.
        'coords': (47, 0, 47, 350),  # top x, y, bottom x, y
        'tics': [2, 4, 9],  # shorts, longs, increment.
        'style': {
            'fill': 'grey',
            'anchor': 'e',
            'width': 1,
        }
    },
    'schematic': {  # This is where all the fancy pointer lines go to show information.
        'geometry': '&_price_matrix',
        'coords': (0, 0),
        'width': 50,
        'height': 349,
        'path_spacing': 20,  # This is how close the lines are allowed to get to one another.
        'path_relief': 5,  # Distance from the target pointer to the start of the line.
        'pointer_relief': -5,  # Distance between line end and the ruler.
        'font': 'Arial 7 normal bold',
        'linetype': 'line',  # More options to come in the future.
        'style': {
            'smooth': True,
            'dash': (1, 2),
            'arrow': 'last',
            'arrowshape': (5, 5, 2),
            'tag_fill': 'grey',
            'outlinestyle': (0, 0, 1, 1),
            'linecolor': 'grey',
            'linethickness': 1,
            'fill': 'black',
        },
        'background': {
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'ticker': {
        'style': {
            'background': 'white',
            'colorup': 'green',
            'colordown': 'red',
            'tickerfont': 'Arial 9 normal bold',
            'tickerfontcolorup': 'black',
            'tickerfontcolordown': 'black',
            'tickerbgup': 'white',
            'tickerbgdown': 'white',
            'quotefont': 'Arial 10 normal bold',
            'quotefontcolorup': 'green',
            'quotebgdown': 'white',
            'quotebgup': 'white',
            'quotefontcolordown': 'red',
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
            'y': 377
            },
        'clear': True,
        'content': '&_alerts',
        'content_type': 'alerts'
    }

}
