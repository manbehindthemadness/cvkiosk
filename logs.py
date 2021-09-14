# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
"""


from pprint import pprint
from pathlib import Path
import traceback
import ntpath
from datetime import datetime


def path_leaf(path):
    """
    Grabs filenames from paths.

    :param path:
    :type path: str
    :return: Filename.
    :rtype: str
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def event_log(event):
    """
    This sends an event message to the UX event log.
    :param event: Whatever the hell you want displayed.
    """
    if event:
        event = str(event).replace('[', '').replace(']', '')
        if '*' in event:
            event = event.split('*')
            event = event[1] + ': ' + event[0]
    return event


def find_level(level: str) -> list:
    """
    THis just returns a list of acceptible log levels.
    """
    l_ord = ['DUMMY', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'DEV']
    result = l_ord
    for i, l_ in enumerate(l_ord):
        if l_ == level:
            result = l_ord[i:]
    return result


class JournalD:
    """
    This is a fancy debug logger.
    """
    def __init__(self, configuration):
        self.settings = configuration
        # Setup log file.
        if self.settings.logfile:
            self.logf = Path(self.settings.logfile)
            self.logf.touch()

        self.l_trans = {
            '*dbug*': 'DEBUG',
            '*info*': 'INFO',
            '*warn*': 'WARNING',
            '*err*': 'ERROR',
            '*crit*': 'CRITICAL',
            '*none*': 'DEV',
            'DEBUG': '*dbug*',
            'INFO': '*info*',
            'WARNING': '*warn*',
            'ERROR': '*err*',
            'CRITICAL': '*crit*',
            'DEV': '*none*'
        }
        self.f_l = find_level(self.settings.log_level_file)
        self.c_l = find_level(self.settings.log_level_console)
        self.e_l = find_level(self.settings.log_level_event)

    def allowed(self, action: list, levels: list) -> list:
        """
        This determines if the log event is within the scope of our settings.
        :param action: The event we will log if allowed.
        :param levels: The list of allowed levels to check.
        """
        result = list()
        wild = action[-1]
        try:
            if '*'not in wild:
                action.append('*none*')
        except ValueError:  # Catch values that aren't strings.
            action.append('*none*')
        token = self.l_trans[action[-1]]
        if token in levels:
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = [dt, token]
            result.extend(action[0:-1])
        return result

    def log(self, *args, dirty: bool = False) -> str:
        """
        Console logger.

        :param args: Fucking agruments..
        :param dirty: in the event we have some weirdness that re-deplodes the arguments into a nested tuple.
        :type args: tuple, str
        """
        zap = 2
        if dirty:
            args = args[0]
        if self.settings.log_locations:
            zap = 3
            stack = traceback.extract_stack()
            line = stack[-2][1]
            filename = path_leaf(stack[-2][0])
            prefix = [filename + ', ' + str(line) + '.']
            args = list(args)
            prefix.extend(args)
            args = prefix
            tuple(args)

        if self.settings.log_info_print:
            if '*pretty*' in args:
                line = args[0:-1]
                pprint(line)
            else:
                console_return = self.allowed(args, self.c_l)
                if console_return:
                    print(console_return)
        if self.logf:
            line = self.allowed(args, self.f_l)
            if line:
                line = str(line) + '\n'
                with open(self.logf, 'a') as lf:
                    lf.write(line)
                lf.close()
        result = str()
        ret = self.allowed(args, self.e_l)
        if ret:
            rt = [ret[1]]
            rt.extend(ret[zap:])
            for b in rt:
                result += str(b) + ' '
        return result
