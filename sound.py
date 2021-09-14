# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
-----------------------------------------------------------------------------------------------------------------------

This is where we will add our buzzer sound alerts.

So this is about the most basic "bit-bang" style alert system, I chose this as there simply isn't space or power
to implement a hardware audio processing solution; however, this may change in the future.

NOTE: We need to keep this between 500 and 2000 hz


"""
import time
from legacy.client import settings
# NOTE: The below warnings are muted as these requirements aren't loaded unless we are on the raspi platform.
# noinspection PyUnresolvedReferences,PyPackageRequirements
import RPi.GPIO as GPIO
from warehouse.logs import JournalD

log = JournalD(settings).log
buz = settings.ALERT_PIN
tm = settings.ALERT_LENGTH


def cycle_buzzer(freq, length):
    """
    This cycles our alert buzzer.

    :param freq: Frenquency to use.
    :param length: Length of alert.
    :return: Nothing.
    """
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    GPIO.setup(buz, GPIO.OUT)
    p = GPIO.PWM(buz, 1000)
    p.ChangeFrequency(freq)
    p.start(settings.VOLUME)
    time.sleep(length)
    p.stop()
    GPIO.cleanup()


def double_high():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(2000, tm)
    time.sleep(0.25)
    cycle_buzzer(2000, tm)


def single_high():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(2000, tm)


def single_low():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(500, tm)


def double_med_high():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(1000, tm)
    cycle_buzzer(2000, tm)


def double_med_low():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(1000, tm)
    cycle_buzzer(500, tm)


def high_med_low():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(2000, tm)
    cycle_buzzer(1000, tm)
    cycle_buzzer(500, tm)


def low_med_high():
    """
    Generic buzzer alert.
    """
    cycle_buzzer(500, tm)
    cycle_buzzer(1000, tm)
    cycle_buzzer(2000, tm)


alerts = {
    'single_high': single_high,
    'double_high': double_high,
    'single_low': single_low,
    'double_med_high': double_med_high,
    'double_med_low': double_med_low,
    'high_med_low': high_med_low,
    'low_med_high': low_med_high,
}


def cycle_alert(alert):
    """
    This kicks off an audio alert and repeats it for the number of times configured in settings.
    :param alert: Name of alert to cycle.
    :type alert: str
    :return: Nothing.
    """
    cycle = settings.ALERT_REPITITION
    alert = alerts[alert]
    while cycle:
        alert()
        time.sleep(1)
        cycle -= 1


if settings.SOUND_TEST and not settings.DEV_MODE:  # Perform sound test.
    log('Performing sound test')
    for a in alerts:
        alerts[a]()
        time.sleep(tm)

log('Successfully loaded sound library')
