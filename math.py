# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""


def get_math():
    """
    This imports eaither numpy or cupy depending on what's around.
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
