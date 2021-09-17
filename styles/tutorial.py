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

EXAMPLE:

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
        'price_canvas_width': '$_screen_width:100%',  # The size of the graphiend canvas.
        'price_canvas_height': '$_screen_height:100%',
        # This scales the candlestick matrix in order to make room for the other widgets.
        'price_matrix_offsets': (50, 50, 35, 150),  # left, right, top, bottom.
        'price_increment': 8,  # The width of one candlestick in pixels.
        'matrices': {},  # These get filled in by the matrix_parser.
        'background': 'grey',
    },
    'asset_order': [  # This is our draw_order widgets will be drawn starting with the farthest back into the foreground.
        'smoothi_bottom',
        'smoothi_top',
        'volume',
        'top_arrows',
        'candlesticks'
    ],
    'actor_order': [  # Animate order for moving actors.
    ],
    # From this point we wil divide this style into sections including the relational configuration respectively.
    'candlesticks': {
        # The bar_width will alter the X coordinates of all the price related widgets.
        'geometry': '&_price_matrix',
        'height': '$_screen_height:50%',
        'color1': 'green',
        'color2': 'red',
        'alpha': 0.75,
        'hollow': ['red']  # This can hole one none or both of the colors.
    },
    'smoothi_bottom': {
        'geometry': '&_price_matrix',
        'height': 200,
        'fill': 'aqua',
        'grad': ('deepskyblue', 'black', 'v'),  # Gradient.
        'graph_type': 'volume',
        'tb': 'b',  # Top or bottom style.
        'outline': 'white',
        'smooth': 5,  # Smooths average out the measurements.
        'lineinterpol': 3,  # Linear interpolation adds points and then rounds off the edges.
        'offset': 50,
        'padding': (47, 0, 0, 0),  # left, right, top, bottom.
        'alpha': 0.2,  # Transparency.
        'alphamask': True,  # Transparency following a gradient.
        'aa': (10, 0)  # Antialiasing (sample_size, passes).
    },
    'smoothi_top': {
        'geometry': '&_price_matrix',
        'height': 50,
        'fill': 'red',
        'graph_type': 'volume',
        'tb': 't',
        'smooth': 1,
        'lineinterpol': 2,
        'offset': 350,
        'padding': (0, 47, 0, 0),
        'alpha': 0.6,
        'aa': (10, 0)
    },
    'volume': {
        'geometry': '&_price_matrix',
        'height': 75,
        'top': 200,
        'bottom': 200,
        'offset': 125,
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
        'fill': 'deepskyblue',
        'thickness': 1,  # Line thickness.
        'arrow': 'first',  # This is the end of the line that thhe arrow will attach.
        'arrowshape': (4, 4, 1),  # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
        'matrix_override': '&_coords1',  # This allows us to pass alternate alert "triggers" instead of just geometry.
        'triggers': '&_triggers1',
        'tb': 't',
        'icon': 'img/icons/minus_circle.png',  # Schematic view icon.
        'icon_fill': 'green',  # Icon color.
        'tag_fill': 'black',  # Schematic text color.
        'use_schematic': False  # Toggle schematics.
    }
}
