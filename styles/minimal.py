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
        'style_name': 'tutorial',  # Name style for organization.
        # Configure global settings in relation to screen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_offset_coord': (0, 0),  # This is the coordinate of the upper left corner of the price canvas.
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:16-',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (2, 2, 30, 75),  # left, right, top, bottom.
        'price_increment': 4,  # The width of one candlestick in pixels.
        'background': 'white',
        'utc_format': '%H:%M:%p',
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'smoothi_bottom',
        'smoothi_top',
        'volume',
        'top_arrows',
        'candlesticks',
        'icing_top1',
        'icing_top2',
        'icing_bottom1',
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
        'coords': (0, 0),  # Uppr left hand corner.
        'border': 0,
        'text_color': 'black',
        'meter_colors_left': "@gp.color_range(0, 100, 'red', 'green')",  # This is an eval statement, it can pass anything in utils.py
        'meter_colors_right': "@gp.color_range(0, 100, 'red', 'green')",
        'meter_label_width_left': 40,
        'meter_label_width_right': 40,
        'font': 'Arial 6 normal bold',
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
    'smoothi_bottom': {
        'geometry': '&_feed_price_matrix',
        'matrix_override': '&_normal_100_1',
        'height': 60,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'blue', 'v'),  # Gradient.
        'graph_type': 'prices',
        'tb': 'b',  # Top or bottom style.
        'outline': 'black',
        'smooth': 1,  # Smooths average out the measurements.
        'lineinterpol': 2,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 160,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        'alpha': 0.2,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_price_matrix',
        'matrix_override': '&_super_drift',
        'height': 20,
        'fill': 'red',
        'graph_type': 'prices',
        'tb': 't',
        'smooth': 2,
        'lineinterpol': 4,
        'offset': 194,
        'padding': (0, 0, 0, 0),  # left, right, top, bottom.
        # 'outline': 'black',
        'alpha': 0.5,
        'aa': (10, 0),
    },
    'volume': {
        'geometry': '&_price_matrix',
        'height': 40,
        'top': 100,
        'bottom': 150,
        'offset': 80,
        'alpha': 0.6,
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
        'triggers': '&_utrends',
        'tb': 't',
        'signal': 'TR.DN',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'green',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': True  # Toggle schematics.
    },
    # 'bottom_arrows': {
    #     'geometry': '&_price_matrix',
    #     'height': 10,
    #     'offset': 10,  # This is the distance the arrow will appear from the coordinate.
    #     'fill': 'magenta',
    #     'thickness': 1,  # Line thickness.
    #     'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
    #     'arrowshape': (5, 5, 2),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
    #     'matrix_override': '&_cl',  # This allows us to pass alternate alert "triggers" instead of just geometry.
    #     'triggers': '&_dtrends',
    #     'tb': 'b',
    #     'signal': 'TR.UP',
    #     'icon': 'img/icons/x1.png',  # Schematic view icon.
    #     'icon_fill': 'red',  # Icon color.
    #     'tag_fill': 'black',  # Schematic text color.
    #     'use_schematic': True  # Toggle schematics.
    # },
    'icing_top1': {
        'geometry': '&_price_matrix',
        'triggers': '&_trend',
        'thickness': 2,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'blueviolet',
        'color2': 'blueviolet',
        'tb': 't'
    },
    'icing_top2': {
            'geometry': '&_price_matrix',
            'triggers': '&_super_trend',
            'thickness': 2,
            'smooth': False,
            'dash': (1, 1),
            'color1': 'black',
            'color2': 'black',
            'tb': 't'
        },
    'icing_bottom1': {
        'geometry': '&_price_matrix',
        'triggers': '&_anti_trend',
        'thickness': 1,
        'smooth': False,
        # 'dash': (1, 1),
        'color1': 'cyan',
        'color2': 'cyan',
        'tb': 'b'
    },
    'tics1': {  # These are the little ruler ticks that run down the edges.
        'coords': (319, 10, 319, 150),  # top x, y, bottom x, y
        'tics': [1, 2, 9],  # shorts, longs, increment.
        'style': {
            'fill': 'black',
            'anchor': 'e',
            'width': 1,
        }
    },
    'date_ruler': {
        'geometry': '&_price_matrix',
        'coords': (320, 150),
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
            'linecolor': 'grey',
            'timelinecolor': 'grey',
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
            'fill': 'white',
            'alpha': 0.1
        }
    },
    'tics2': {  # These are the little ruler ticks that run down the edges.
        'coords': (0, 10, 0, 150),  # top x, y, bottom x, y
        'tics': [1, 2, 9],  # shorts, longs, increment.
        'style': {
            'fill': 'black',
            'anchor': 'w',
            'width': 1,
        }
    },
    'ticker': {
        'style': {
            'background': 'white',
            'colorup': 'green',
            'colordown': 'red',
            'tickerfont': 'Arial 6 normal bold',
            'tickerfontcolorup': 'black',
            'tickerfontcolordown': 'black',
            'tickerbgup': 'white',
            'tickerbgdown': 'white',
            'quotefont': 'Arial 6 normal bold',
            'quotefontcolorup': 'green',
            'quotebgdown': 'white',
            'quotebgup': 'white',
            'quotefontcolordown': 'red',
            'iconup': None,
            'icondown': None,
            'symbolup': '▲',
            'symboldown': '▼',
            'symbolwidth': None,
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
