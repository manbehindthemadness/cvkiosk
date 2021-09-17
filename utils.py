# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import os
import re
import configparser
import importlib

WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


def get_math():
    """
    This imports either numpy or cupy depending on what's around.
    :return: math module
    """
    try:
        # noinspection PyPackageRequirements
        import cupy as mm  # This is for brutal math performance in the event we are running on a jetson.
    except ImportError:
        import numpy as mm  # This is the standard shit for everything else.
    return mm


np = get_math()


def nparray(lst: [list, np.array]) -> np.array:
    """
    This is an array conversion wrapper that allows us to send arrays to both numpy and cupy.
    :param lst: List to be converted.
    :return: array
    """
    def _iter(_lst: list) -> list:  # TODO: We changed this, keep an eye on it.
        """
        This iterates down sublists.
        :param _lst: Sublist.
        """
        if not isinstance(_lst, list):
            _lst = list(lst)
        for idx, item in enumerate(_lst):
            # Bro, what were we thinking here... This is improper type checking.
            if str(type(item)) == "<class 'cupy._core.core.ndarray'>" or str(type(item)) == "<class 'numpy.ndarray'>":
                _lst[idx] = _iter(item)
        return _lst
    result = np.array(lst)
    return result


def percent_of(percent, whole, use_float=False):
    """
    Generic math method
    """
    result = np.divide(np.multiply(percent, whole), 100.0)
    if not use_float:
        result = int(result)
    return result


def percent_in(part, whole, use_float=False):
    """
    Generic math method
    """
    result = np.multiply(100.0, np.divide(part, whole))
    if not use_float:
        result = int(result)
    return result


def config(section: str) -> configparser:
    """
    Thius will grab our settings.
    :return:
    """
    cfg = configparser.ConfigParser()
    cfg.read(WORKING_DIR + '/cfg.ini')
    cfg = cfg[section]
    settings = dict()
    for setting in list(cfg.keys()):
        try:
            value = eval(cfg[setting])
        except SyntaxError:
            value = cfg[setting]
        settings.update({setting: value})
    return settings


def list_key_lookup(lst: list, dct: dict):
    """
    This will use an eval statement to lookup a series of sub-keys using a list.
    """
    dct.keys()
    keys = str()
    for key in lst:
        keys += "['" + str(key) + "']"
    exp = 'dct' + keys
    result = eval(exp)
    return result


def num(exp: str) -> float:
    """
    Simple regex to pull only the numbers out of a string
    """
    return float(re.findall(r'\d+', exp)[0])


def evaluate_expression(expression, style: dict, constants: dict):
    """
    This will basically check to see if we have an expression, if so we will return the evaluated result.
    """
    result = expression
    lookup = style
    if '$' in str(expression):
        sp = expression.split(':')
        keys = sp[0].split('$')[1:]
        if keys[-1][0] == '_':
            lookup = constants
        lookup_value = list_key_lookup(keys, lookup)
        try:
            formula = sp[1]
            if "%" in formula:  # Get percentage.
                result = percent_in(num(formula), lookup_value)
            elif '-' in formula:  # Subtract.
                result = np.subtract(lookup_value, num(formula))
            elif '+' in formula:  # Add.
                result = np.add(lookup_value, num(formula))
            elif '*' in formula:  # Multiply.
                result = np.multiply(lookup_value, num(formula))
            elif '\\' in formula:  # Divide.
                result = np.divide(lookup_value, num(formula))
            else:
                result = lookup_value
        except IndexError:
            result = lookup_value
    elif '@' in str(expression):
        result = eval(expression.replace('@', ''))
    return result


def style_iter(style: dict, constants: dict) -> dict:
    """
    This will take all the variable expressions in our style, figure the math and return the result.

    Note that when call a value it will be from r_style as it will relay the original dictionary as we iterate through
        sub-keys.
    """
    result = dict()
    for key in style:
        if isinstance(style[key], dict):
            result[key] = style_iter(style[key], constants)
        else:
            result[key] = evaluate_expression(style[key], style, constants)
    return result


def style_parser(style: str, constants: dict):
    """
    This uses style_iter and the above functions to construct a fully evaluated style sheet.
    """
    cmd = 'styles.' + str(style)
    style = importlib.import_module(cmd)
    # noinspection PyUnresolvedReferences
    style = style.style
    result = style_iter(style, constants)
    return result


def constants_parser(constants_str: [str, dict]) -> dict:
    """
    This will get the constants for a specific display type and add in whatever geometry we want to call in the style.
    """
    constants = importlib.import_module('constants.' + constants_str)
    # noinspection PyUnresolvedReferences
    result: dict = constants.constants
    return result


def layout_parser(layout: str):
    """
    This will pull us a layout based on what we pass from settings.
    """
    layout = importlib.import_module('layouts.' + layout)
    # noinspection PyUnresolvedReferences
    return layout.Format


def evaluate_matrix(expression: str, main: dict):
    """
    This will take a matrix expression and populate it based on the calculated values in style['main']
    """
    result = expression
    if '&' in str(expression):
        result = main[expression.replace('&', '')]
    return result


def matrix_iter(style: dict, main: dict) -> dict:
    """
    This will iterate the style and fill in the requested matrices.
    """
    result = dict()
    for key in style:
        if isinstance(style[key], dict):
            result[key] = matrix_iter(style[key], main)
        else:
            result[key] = evaluate_matrix(style[key], main)
    return result


def matrix_parser(style: dict, matrices: dict) -> dict:
    """
    This will update the style['main'] with the newly constructed matrices and then update the style accordingly.
    """
    style['main'].update(matrices)
    main = style['main']
    style = matrix_iter(style, main)
    return style
