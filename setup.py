# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
------------------------------------------------------------------------------------------------------------------------
*This file is a work in progress and likely doesn't meet general standards.*

TODO: This is nowhere near proper, but I was in a rush...

Reference:
1. https://packaging.python.org
2. https://julien.danjou.info/starting-your-first-python-project/
3. https://medium.com/@trstringer/the-easy-and-nice-way-to-do-cli-apps-in-python-5d9964dc950d
4. https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
5. https://python-packaging.readthedocs.io
6. https://github.com/pypa/sampleproject
7. https://pypi.org/classifiers/
8. https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
"""

import sys
import os
import sysconfig
import shutil
from subprocess import Popen, PIPE
from setuptools import setup, find_packages
from setuptools.command.install import install
from pathlib import Path

here = Path(os.path.abspath(os.path.dirname(__file__)))
there = Path(str(sysconfig.get_paths()["purelib"]) + '/cvkiosk')
version = 0.1


def system_command(params):
    """
    Use this to execute a system level command.

    NOTE: Use with caution.
    :param params: List of commands and args to execute.
    :type params: list
    :return: stout.
    :rtype: PIPE
    """
    process = Popen(params, stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode("utf8")
    return output


def is_virtualenv():
    """
    https://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
    """
    if hasattr(sys, 'real_prefix'):
        return True
    if hasattr(sys, 'base_prefix'):
        return sys.prefix != sys.base_prefix
    return False


def is_superuser():
    """
    Aptly named.
    :return:
    """
    return os.getuid() == 0


def simple_install(installer, obj, copy=False):
    """
    Place files into site-packages.
    """
    def place_files():
        """
        Just that...
        :return:
        """
        try:
            shutil.rmtree(there)
        except WindowsError:
            pass
        # system_command(['pip', 'install', '-r', 'requirements.txt'])
        shutil.copytree(
            here,
            there,
            ignore=shutil.ignore_patterns('*.git', '*.idea', '*.gitignore', '*graphiend.egg-info')
                        )

    if copy:
        place_files()
    installer.run(obj)


class Install(install):
    """
    Our installer :)
    """
    def run(self):
        """
        TODO: Write an uninstaller...
        """
        simple_install(install, self, True)


class Uninstall(install):
    """
    Our installer :)
    """
    def run(self):
        """
        TODO: Write an uninstaller...
        """
        shutil.rmtree(there)


# Configuration setup module
setup(
    name="graphiend",
    version=version,
    author="Manbehindthemadness",
    author_email="",
    description="A general use graphing library based on PIL and TkInter",
    packages=find_packages(exclude=['graphiend.tests']),  # Required
    package_data={"graphiend": ["graphiend_variables", "graphiend_libraries"]},
    # Requisites
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    platforms=["linux", "linux2", "darwin"],
    # Zip safe configuration
    # https://setuptools.readthedocs.io/en/latest/setuptools.html#setting-the-zip-safe-flag
    zip_safe=False,
    # Install extra scripts
    cmdclass={
        'install': Install,
        'uninstall': Uninstall

              },
)
# EOF
