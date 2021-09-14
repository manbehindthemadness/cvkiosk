# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""
import os
import configparser


WORKING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))


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
