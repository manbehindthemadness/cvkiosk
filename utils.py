# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------
"""
import os
import re
import signal
import time
import configparser
import importlib
import datetime
import logging
import random
import requests
import urllib.request
from urllib.error import URLError
import bs4
import socket
from subprocess import Popen, PIPE
import numpy as np
from pathlib import Path

import graphiend as gp # noqa

WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
logging.getLogger().setLevel(logging.INFO)
FGI = 0


def overwrite_to_file(filename: Path, data: str):
    """
    This will write/overwrite a line of text to a file.
    """
    with open(filename.as_posix(), 'w') as file:
        file.write(data)


def test_o_random(view_arry: list, alerts: int) -> list:
    """
    This creates random alert arrays for testing.
    """
    def rand_val(randstat: float) -> float:
        """
        Throws out a random value from 1-25
        """
        res = 0
        if not random.randint(0, int(randstat)):
            res = random.randint(1, 25)
        return res

    ll = len(view_arry)
    rand_stat = ll / alerts
    sett: list = [0] * ll
    for idx, s in enumerate(sett):
        s = rand_val(rand_stat)
        sett[idx] = s
    return sett


def clean_args(args: list, kwargs: dict, exclusive: bool = False) -> dict:
    """
    Removes keys top prevent errors.
    """
    kargs = list(kwargs.keys())
    if exclusive:
        for arg in kargs:
            if arg not in args:
                del kwargs[arg]
    else:
        for arg in args:
            try:
                del kwargs[arg]
            except KeyError:
                pass
    return kwargs


def get_args(args: list, kwargs: dict, clean: bool = False) -> list:
    """
    This will fetch arguments and jazz.
    """
    values = list()
    for arg in args:
        if arg in kwargs:
            values.append(kwargs[arg])
        else:
            values.append(None)
    if clean:
        clean_args(args, kwargs)
    if len(values) == 1:
        values = values[0]
    return values


def log(*args, **kwargs):
    """
    Really simple-ass logger.
    """

    message = str()
    for arg in args:
        message += str(arg) + ' '
    level = get_args(
        ['level'],
        kwargs
    )
    if not level:
        level = 'info'
    cmd = 'logging.' + level + '(message)'
    exec(cmd)


def system_command(params, shell: bool = False) -> str:
    """
    Use this to execute a system level command.

    NOTE: Use with caution.
    """
    process = Popen(params, stdout=PIPE, shell=shell)
    output, _error = process.communicate()
    output = output.decode("utf8")
    return output


def safelaunch(operation, kwargs, condition: bool):
    """
    Safe launches a thread, but skips for development testing based on 'condition'
    """
    if condition:
        operation(**kwargs)
    else:
        if __name__ == '__main__':
            operation(**kwargs)


class Term:
    """
    This watches for a service termination signal
    """
    term = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal)
        signal.signal(signal.SIGTERM, self.signal)

    # noinspection PyUnusedLocal
    def signal(self, *args):
        """
        Signal callback.
        """
        self.term = True


def safesleep(sig: Term, duration: int):
    """
    A sleep loop that can be terminated with a closure switch
    """
    while duration and not sig.term:
        time.sleep(1)
        duration -= 1


def nparray(lst: [list, np.array]) -> np.array:
    """
    This is an array conversion wrapper that allows us to send arrays to both numpy and cupy.
    :param lst: List to be converted.
    :return: array
    """
    def _iter(_lst: list) -> list:
        """
        This iterates down sublists.
        :param _lst: Sublist.
        """
        if not isinstance(_lst, list):
            _lst = list(lst)
        for idx, item in enumerate(_lst):
            # This type checking is totally improper, but as only one of these imports exist we are forced...
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


def read_config_file(section: str, file: str) -> dict:
    """
    This will pull the settings from individual files.
    """
    cfg = configparser.ConfigParser()
    cfg.read(file)
    cfg = cfg[section]
    settings = dict()
    for setting in list(cfg.keys()):
        try:
            value = eval(cfg[setting])
        except SyntaxError:
            value = cfg[setting]
        settings.update({setting: value})
    return settings


def config(section: str) -> configparser:
    """
    This will grab our settings.
    :return:
    """
    settings = read_config_file(section, WORKING_DIR + '/def.ini')
    local = read_config_file(section, WORKING_DIR + '/cfg.ini')
    settings.update(local)
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


def mk_arry(arry):
    """
    This converts whatever it can into a numpy array.
    """
    if isinstance(arry, (np.ndarray, list, tuple)):
        try:
            arry = np.array(arry)
        except AttributeError:
            pass
    return arry


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
        try:  # TODO: We need to add static arithmatic into the base_style as we don't need to process it each redraw.
            formula = sp[1]
            if "%" in formula:  # Get percentage.
                result = percent_of(num(formula), lookup_value)
                pass
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
    elif '@' in str(expression):  # TODO: Probably need to evaluate these for security reasons.
        result = eval(expression.replace('@', ''))
    elif '@@' in str(expression):
        result = exec(expression.replace('@@', ''))
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
        result = mk_arry(main[expression.replace('&', '')])
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


def matrix_sorter(price_matrix, matrices: dict, prefix: str = None) -> dict:
    """
    This will sort all the coords from the price matrix and add them to the matrices' dictionary.
    Output coordinate map:
                    lu -- cu -- ru
                    |           |
                    lt          rt
                    |           |
                    lc    ac    rc
                    |           |
                    lb          rb
                    |           |
                    ll -- cl -- rl
    """
    coords = ['lu', 'cu', 'ru', 'rt', 'rc', 'rb', 'rl', 'cl', 'll', 'lb', 'lc', 'lt', 'ac']
    if not prefix:
        prefix = '_'
    else:
        prefix = '_' + prefix + '_'
    for coord, matrix in zip(coords, np.array(price_matrix.price_matrix)):
        matrices[prefix + coord] = np.array(matrix)

    matrices[prefix + 'price_matrix'] = price_matrix
    matrices[prefix + 'volume'] = np.array(price_matrix.volume)
    matrices[prefix + 'prices'] = np.array(price_matrix.prices)
    matrices[prefix + 'volume_quote'] = [price_matrix.volume[-1]]
    matrices[prefix + 'price_quote'] = [price_matrix.prices[-1]]
    matrices[prefix + ''] = np.array(price_matrix.adjusted_price_points)
    return matrices


def ticks_to_chart_time(ticks: int) -> str:
    """
    This converts datetime ticks into a timestamp that can be used in our charting files.
    """
    stamp = datetime.datetime.now() + datetime.timedelta(microseconds=np.divide(ticks, 10))
    return stamp.strftime("%Y-%m-%d-%H-%M")


def flip_stream(stream: np.array) -> np.array:
    """
    This will take a stream of coords (x, y, x, y, x, y) and flip it vertically.
    """
    result = np.linspace(0, 0, num=len(stream))
    xs = stream[0::2]
    ys = stream[1::2]
    mi, ma = np.amin(ys), np.amax(ys)
    np.subtract(ys, mi)
    np.multiply(ys, -1)
    np.add(ys, ma)
    result[0::2] = xs
    result[1::2] = ys
    return result


def get_from_html(url: str, criteria: tuple):
    """
    This gets the target criteria from the html stored at the specified URL.
    """
    try:
        page = urllib.request.urlopen(url).read()
        soup = bs4.BeautifulSoup(page, "html.parser")
        div = soup.find(*criteria)
        result = div.contents
    except (AttributeError, socket.gaierror, URLError, requests.exceptions.ConnectionError):
        pass
        result = ''
    return result


def get_index():
    """
    This grabs out fear and greed index
    :return: Index value.
    :rtype: int
    """
    global FGI
    try:
        fgi = int(get_from_html('https://alternative.me/crypto/fear-and-greed-index/', ("div", {"class": "fng-circle"}))[0])
        FGI = fgi
    except (IndexError, TypeError, AttributeError):
        fgi = FGI
    return fgi


def get_median(arry: np.array) -> [int, float]:
    """
    This will return the most common element in a list
    """
    return max(set(arry), key=arry.count)


def filter_wicks(matrix: np.ndarray, multiplier: [int, float] = 2) -> np.ndarray:
    """
    This will filter out impossible spike values that occasionally pollute the data.
    """
    range_max = np.max(matrix[:, 4])
    range_min = np.min(matrix[:, 4])
    high_limit = np.multiply(range_max, multiplier)
    low_limit = np.divide(range_min, multiplier)

    condition_high = matrix[:, 2] >= high_limit  # Filter highs.
    matrix[condition_high, 2] = matrix[condition_high, 1]
    condition_low = matrix[:, 3] >= low_limit  # Filter lows.
    matrix[condition_low, 3] = matrix[condition_low, 4]
    return matrix
