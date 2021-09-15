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

Be aware that many of the naming conventions for the various parameters here are defined by third party logic and
    a result of this there is no standard naming convention. This will be corrected in a future build.
"""

example_constants = {  # This is an example of the constants dictionary (not the one we actually use ;).
    '_screen_size': '400x500',
    '_screen_height': 400,
    '_screen_width': 500,
    '_price_matrix': 'example from chart-to-pix',
}


style_base = {
    'main': {
        'style_name': 'tutorial',  # Name style for organization.
        # Configure global settings in relation to streen size and what have you.
        'geometry': "$_screen_size:",  # This is our screen size.
        'price_canvas_width:': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': 350,
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (50, 50, 35, 150),  # left, right, top, bottom.
    },
    # From this point we wil divide this style into sections including the relational configuration respectively.
    'candlesticks': {
        # The bar_width will alter the X coordinates of all the price related widgets.
        'bar_width': 8,  # The width of one candlestick in pixels.
        'geometry': '$_price_matrix:',
        'height': '$_screen_height:50%',
        'color_1': 'green',
        'color_2': 'red',
        'alpha': 0.75,
        'hollow': ['red']  # This can hole one none or both of the colors.
    },
    'smoothi_bottom': {
        'geometry': '$_price_matrix:',
        'height': 75,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'black', 'v'),
        'graph_type': 'volume',
        'tb': 'b',
        'outline': 'white',
        'smooth': 5,
        'lineinterpol': 3,
        'offset': 300,
        'padding': (47, 47, 0, 0),  # left, right, top, bottom.
        'alpha': 0.2,
        'alphamask': True,
        'aa': (10, 0)
    }
}
