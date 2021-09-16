# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------

This is full of aptly named test code.
"""
from utils import (
    config,
    style_parser,
    constants_parser,
    layout_parser
)

config = config('settings')

constants = constants_parser(  # Get screen and geometry constants.
    config['constants'],
    {'_triggers1': {}}
)

layout = layout_parser(  # Get layout widgets.
    config['layout']
)

style = style_parser(  # Get style sheet.
    'tutorial',
    constants
)