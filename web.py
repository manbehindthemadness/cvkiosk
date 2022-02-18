# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
-----------------------------------------------------------------------------------------------------------------------

This is where we screw around with things.
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import shutil
from pathlib import Path
import time
import random
import flask
import glob
import os
import logging
import sys

old_name = str()
image_directory = './www'
base = 'www/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(base))]
static_image_route = '/www/'


def clean_images(alll: bool = False):
    """
    Flushes out old images.
    """
    print('images', list_of_images)
    for image in list_of_images:
        if image == 'chart.png' and not alll:
            pass
        else:
            try:
                os.remove(base + image)
                print('removing image', base + image)
            except FileNotFoundError:
                pass


clean_images(alll=True)


def run_dash(settings):
    """
    Launches debug webserver.
    :return: Nothing.
    """
    logger = logging.getLogger('ext_dash')
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    if settings['debug_web']:
        log = print
    else:
        log = logger.info

    refresh_time = settings['webserver_refresh'] * 60 * 1000
    clean_images()
    app = dash.Dash(__name__)
    app.external_stylesheets = 'css/style.css'
    app.scripts.config.serve_locally = False

    app.layout = html.Div([
        html.Div(id='screen'),
        dcc.Interval(
            id='interval-component',
            interval=refresh_time,  # in milliseconds
            n_intervals=0
        ),
    ])

    # noinspection PyUnusedLocal
    @app.callback(
        dash.dependencies.Output('screen', 'children'),
        dash.dependencies.Input('interval-component', 'n_intervals')
    )
    def ref(value):
        """
        Basically this copies a temp image from the original to fool the browser into reloading it.

        :param value:
        :return:
        """
        global old_name
        global list_of_images

        tell = Path(base + 'chart.png')
        exist = False
        good = 10
        name = None
        while not exist:  # TODO: This needs to be performed via image content matching.
            name = str(random.randint(0, 20000)) + '.png'
            if tell.is_file():
                try:
                    shutil.copy(base + 'chart.png', base + name)
                    if old_name:
                        os.remove(base + old_name)
                    old_name = name
                    list_of_images = [name]
                    exist = True
                except FileNotFoundError as err:
                    log('file copy error', err)
                    pass
            good -= 1
            if not good:
                log('unable to copy file, error:', name)
            time.sleep(0.5)
        log('file copy success')

        return html.Img(id='graph', src='/www/' + name, style={'width': '100%'}),

    # Add a static image route that serves images from desktop
    # Be *very* careful here - you don't want to serve arbitrary files
    # from your computer or server

    @app.server.route('{}<image_path>.png'.format(static_image_route))
    def serve_image(image_path):
        """
        Fucking docstring
        :param image_path:
        :return:
        """
        global list_of_images
        image_name = '{}.png'.format(image_path)
        # if image_name not in list_of_images:
        if '.png' not in image_name:
            raise Exception(str(image_name) + ' is excluded from the allowed static files'.format(image_path))
        return flask.send_from_directory(image_directory, image_name)

    app.run_server(host='0.0.0.0')
