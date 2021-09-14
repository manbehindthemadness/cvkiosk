# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.

This program is experimental and proprietary, redistribution is prohibited.
Please see the license file for more details.
-----------------------------------------------------------------------------------------------------------------------

This is basically a rewrite of the pisugar2 stuff into something remotely usable...

Default register configurations:
Note: 0x~ means the register is returning a fluctuating value.
{
'0x0': '0xea', '0x1': '0xfe', '0x2': '0x7b', '0x3': '0x68', '0x4': '0xb7',
'0x5': '0x0', '0x6': '0x9c', '0x7': '0x0', '0x8': '0x0', '0x9': '0x4',
'0xa': '0x7e', '0xb': '0x62', '0xc': '0x43', '0xd': '0x0', '0xe': '0x0',
'0xf': '0x0', '0x10': '0xd9', '0x11': '0xba', '0x12': '0x1', '0x13': '0x0',
'0x14': '0x80', '0x15': '0x33', '0x16': '0x0', '0x17': '0x84', '0x18': '0x0',
'0x19': '0x0', '0x1a': '0x0', '0x1b': '0x0', '0x1c': '0x0', '0x1d': '0x0',
'0x1e': '0x0', '0x1f': '0x0', '0x20': '0xfa', '0x21': '0x2e', '0x22': '0x52',
'0x23': '0x48', '0x24': '0x85', '0x25': '0xd7', '0x26': '0xff', '0x27': '0x93',
'0x28': '0x0', '0x29': '0x0', '0x2a': '0x0', '0x2b': '0x0', '0x2c': '0x0',
'0x2d': '0x0', '0x2e': '0x0', '0x2f': '0x0', '0x30': '0xfe', '0x31': '0xb4',
'0x32': '0x52', '0x33': '0xab', '0x34': '0x9c', '0x35': '0x9d', '0x36': '0x85',
'0x37': '0x82', '0x38': '0xfd', '0x39': '0x6d', '0x3a': '0x14', '0x3b': '0x0',
'0x3c': '0x0', '0x3d': '0x0', '0x3e': '0x0', '0x3f': '0x0', '0x40': '0x52',
'0x41': '0xa', '0x42': '0x11', '0x43': '0x23', '0x44': '0xd5', '0x45': '0x0',
'0x46': '0x0', '0x47': '0x0', '0x48': '0x0', '0x49': '0x0', '0x4a': '0x1f',
'0x4b': '0x55', '0x4c': '0x1', '0x4d': '0x0', '0x4e': '0x0', '0x4f': '0x0',
'0x50': '0x5', '0x51': '0x0', '0x52': '0x0', '0x53': '0x0', '0x54': '0x0',
'0x55': '0x0', '0x56': '0x0', '0x57': '0x0', '0x58': '0x0', '0x59': '0x0',
'0x5a': '0x0', '0x5b': '0x0', '0x5c': '0x0', '0x5d': '0x0', '0x5e': '0x0',
'0x5f': '0x0', '0x60': '0x0', '0x61': '0x0', '0x62': '0x0', '0x63': '0x0',
'0x64': '0x0', '0x65': '0x0', '0x66': '0xff', '0x67': '0x0', '0x68': '0x0',
'0x69': '0x0', '0x6a': '0x0', '0x6b': '0x0', '0x6c': '0x0', '0x6d': '0x0',
'0x6e': '0x0', '0x6f': '0x0', '0x70': '0x25', '0x71': '0x0', '0x72': '0x1c',
'0x73': '0xe0', '0x74': '0x1b', '0x75': '0x0', '0x76': '0xc', '0x77': '0x0',
'0x78': '0x15', '0x79': '0x0', '0x7a': '0x1', '0x7b': '0x70', '0x7c': '0x3',
'0x7d': '0x6', '0x7e': '0x0', '0x7f': '0x11', '0x80': '0x53', '0x81': '0x66',
'0x82': '0x86', '0x83': '0xaf', '0x84': '0x5a', '0x85': '0x72', '0x86': '0xa4',
'0x87': '0x5f', '0x88': '0x91', '0x89': '0x0', '0x8a': '0x0', '0x8b': '0x0',
'0x8c': '0x0', '0x8d': '0x0', '0x8e': '0x0', '0x8f': '0x0', '0x90': '0x7f',
'0x91': '0x8c', '0x92': '0xa6', '0x93': '0xd0', '0x94': '0x84', '0x95': '0x97',
'0x96': '0xc4', '0x97': '0x87', '0x98': '0xb0', '0x99': '0x0', '0x9a': '0x0',
'0x9b': '0x0', '0x9c': '0x0', '0x9d': '0x0', '0x9e': '0x0', '0x9f': '0x0',
'0xa0': '0x~', '0xa1': '0x~', '0xa2': '0x~', '0xa3': '0x18', '0xa4': '0x~',
'0xa5': '0x3d', '0xa6': '0x34', '0xa7': '0x2c', '0xa8': '0xbe', '0xa9': '0x15',
'0xaa': '0x10', '0xab': '0x~', '0xac': '0x~', '0xad': '0x1a', '0xae': '0x0',
'0xaf': '0x0', '0xb0': '0x0', '0xb1': '0x0', '0xb2': '0x0', '0xb3': '0x0',
'0xb4': '0x0', '0xb5': '0x0', '0xb6': '0x0', '0xb7': '0x0', '0xb8': '0x0',
'0xb9': '0x0', '0xba': '0x0', '0xbb': '0x0', '0xbc': '0x0', '0xbd': '0x0',
'0xbe': '0x0', '0xbf': '0x0', '0xc0': '0x0', '0xc1': '0x0', '0xc2': '0x0',
'0xc3': '0x0', '0xc4': '0x0', '0xc5': '0x0', '0xc6': '0x0', '0xc7': '0x0',
'0xc8': '0x0', '0xc9': '0x0', '0xca': '0x0', '0xcb': '0x0', '0xcc': '0x0',
'0xcd': '0x0', '0xce': '0x0', '0xcf': '0x0', '0xd0': '0x0', '0xd1': '0x0',
'0xd2': '0x0', '0xd3': '0x0', '0xd4': '0x0', '0xd5': '0x0', '0xd6': '0x0',
'0xd7': '0x0', '0xd8': '0x0', '0xd9': '0x0', '0xda': '0x0', '0xdb': '0x0',
'0xdc': '0x0', '0xdd': '0x0', '0xde': '0x0', '0xdf': '0x0', '0xe0': '0x0',
'0xe1': '0x0', '0xe2': '0x0', '0xe3': '0x0', '0xe4': '0x0', '0xe5': '0x0',
'0xe6': '0x0', '0xe7': '0x0', '0xe8': '0x0', '0xe9': '0x0', '0xea': '0x0',
'0xeb': '0x0', '0xec': '0x0', '0xed': '0x0', '0xee': '0x0', '0xef': '0x0',
'0xf0': '0x0', '0xf1': '0x0', '0xf2': '0x0', '0xf3': '0x0', '0xf4': '0x0',
'0xf5': '0x0', '0xf6': '0x0', '0xf7': '0x0', '0xf8': '0x0', '0xf9': '0x0',
'0xfa': '0x0', '0xfb': '0x0', '0xfc': '0x0', '0xfd': '0x0', '0xfe': '0x0'
}
Documented register defaults:
{
'0x1': '234 h 0xea b 0b11101010',
'0x2': '254 h 0xfe b 0b11111110',
'0x3': '123 h 0x7b b 0b1111011',
'0x4': '104 h 0x68 b 0b1101000',
'0x7': '156 h 0x9c b 0b10011100',
'0xc': '98 h 0x62 b 0b1100010',
'0x22': '46 h 0x2e b 0b101110',
'0x24': '72 h 0x48 b 0b1001000',
'0x25': '133 h 0x85 b 0b10000101',
'0x26': '215 h 0xd7 b 0b11010111',
'0x51': '5 h 0x5 b 0b101',
'0x52': '0 h 0x0 b 0b0',
'0x53': '0 h 0x0 b 0b0',
'0x54': '0 h 0x0 b 0b0',
'0x55': '0 h 0x0 b 0b0',
'0x71': '37 h 0x25 b 0b100101',
'0x72': '0 h 0x0 b 0b0',
'0x77': '12 h 0xc b 0b1100',
'0xa2': '0 h 0x~ b ????????',
'0xa3': '0 h 0x~ b ????????',
'0xa4': '24 h 0x18 b 0b11000',
'0xa5': '0 h 0x~ b ????????',
'0xa8': '44 h 0x2c b 0b101100',
'0xa9': '190 h 0xbe b 0b10111110'
}
MODIFIED REGISTERS: (from sugar that has been messed with).
{
'0x1': '234 h 0xea b 0b11101010',
'0x2': '254 h 0xfe b 0b11111110',
'0x3': '123 h 0x7b b 0b1111011',
'0x4': '104 h 0x68 b 0b1101000',
'0x7': '157 h 0x9d b 0b10011101', -
'0xc': '98 h 0x62 b 0b1100010',
'0x22': '46 h 0x2e b 0b101110',
'0x24': '72 h 0x48 b 0b1001000',
'0x25': '133 h 0x85 b 0b10000101',
'0x26': '215 h 0xd7 b 0b11010111',
'0x51': '5 h 0x5 b 0b101',
'0x52': '1 h 0x1 b 0b1', -
'0x53': '20 h 0x14 b 0b10100', -
'0x54': '63 h 0x3f b 0b111111', -
'0x55': '0 h 0x0 b 0b0',
'0x71': '37 h 0x25 b 0b100101',
'0x72': '0 h 0x0 b 0b0',
'0x77': '12 h 0xc b 0b1100',
'0xa2': '0 h 0x~ b ????????',
'0xa3': '0 h 0x~ b ????????',
'0xa4': '24 h 0x18 b 0b11000',
'0xa5': '0 h 0x~ b ????????',
'0xa8': '44 h 0x2c b 0b101100',
'0xa9': '57 h 0x39 b 0b111001' -
}

NOTE: THis file is a mess, but it''s the best I could do without any form of real documentation...
        I really wish I could figure out how to get the programmable button to work, but at this point
        it's just eating too much of the project schedule.

        TODO: Clean up all the old math comments after we confirm our numpy conversion is working properly.

        0x53: GPIO4_INEN: 0: disable: 1: enable (GPIO4 input toggle)
        0x54: GPIO4_OUTEN: 0: disable: 1: enable (GPIO output toggle)
        0x55: GPIO4_DAT: (GPIO4 data output pin)


    /// Is power cable plugged in
    pub fn is_power_plugged_2led(&self) -> Result<bool> {
        let v = self.i2c.smbus_read_byte(0x55)?;
        if v & 0b0001_0000 != 0 {
            return Ok(true);
        }
        Ok(false)
    }

    /// Read gpio tap 4:0, gpio4 / gpio1
    pub fn read_gpio_tap(&self) -> Result<u8> {
        let v = self.i2c.smbus_read_byte(0x55)?;
        Ok(v)

        bus.write_byte_data(0x75, 0x54, 1)
        bus.write_byte_data(0x75, 0x53, 0)

        if 0x53 is 191 charge detection works
        and
        if 0x52 is 20 charge detection works


        OK Here is the skinny:::
        with
            0x52 = 0x14(20)
            0x53 = 0x3f(63) - 191 seems to be a better value....
        the multifunction button works on register 0xa6...Oddly the only one not in the documentation...
        button down seems to be returning values in the 70s I think it has to do with the length of the press,,,
        long button down returns 82
        button up seems to be returning 74
        writing 64 seems to reset all three pins...
        NOTE: Long press seems to be the only reliable return here, the others seem to return without warning at times...



"""
# noinspection PyPackageRequirements
from smbus2 import SMBus
# import threading
from legacy.client import settings
from math import percent_in
from logs import JournalD
import numpy as np

log = JournalD(settings).log


class Sugar:
    """
    This is my attempt to create a somewhat usable PiSugar2 driver...

    I hate to say it but I am going to have to use the bundled power manager in rust.
    The documentation on the controller chip is just not there...

    https://github.com/kellertk/pwnagotchi-plugin-pisugar2/blob/main/pisugar2.py
    """

    RTC_ADDRESS = 0x32
    BAT_ADDRESS = 0x75
    GPIO_1 = 0x53
    CHARGING_REGISTER = 0x55  # GPIO_4 also enables /disables charging.
    GPIO_2 = 0x54

    # 0b1111_1011 Enable
    # 0b0000_0100 Disable
    CTR1 = 0x0f
    CTR2 = 0x10
    CTR3 = 0x11
    TAP_ARRAY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    GPIO_INTERVAL = 0.5
    BATTERY_LEVEL = 0
    EVENT = None
    CHARGING = 0
    PRESS = False

    def __init__(self):
        # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self._bus = SMBus(1)
        self._is_pro = False

    def voltage(self):
        """
        This gets the voltage from the battery unit
        :return:
        """
        try:
            address = self.BAT_ADDRESS
            if self._is_pro:
                low = self._bus.read_byte_data(address, 0x64)
                high = self._bus.read_byte_data(address, 0x65)
            else:
                low = self._bus.read_byte_data(address, 0xa2)
                high = self._bus.read_byte_data(address, 0xa3)
            if high & 0x20:
                low = ~low & 0xff
                high = ~high & 0x1f
                v = np.add(((high | 0b1100_0000) << 8), low)
                result = np.divide(
                    np.subtract(
                        2600.0,
                        np.multiply(v, 0.26855)
                    ),
                    1000
                )
            else:
                v = np.add(((high & 0x1f) << 8), low)
                result = np.divide(
                    np.add(
                        2600.0,
                        np.multiply(v, 0.26855)
                    ),
                    1000
                ), self._bus.read_byte_data(address, 0x55)
        except ValueError as err:
            log(err, '*err*')
            result = 0.0
        return result

    @staticmethod
    def reserve(batt_lvl):
        """
        This calculates the percentage of remaining battery excluding the reserve before automatic shutdown
        that is specified in the client.settings file.
        :param batt_lvl: This is the raw percentage of battery remaining.
        :type batt_lvl: int, float
        :return: Percentage remaining.
        :rtype: float
        """
        base = np.round(
            np.subtract(batt_lvl, settings.SHUTDOWN_PERCENT),
            1
        )
        percentage = percent_in(
            base,
            np.subtract(100, settings.SHUTDOWN_PERCENT),
            use_float=True
        )
        result = float(np.round(percentage, 1))
        return result

    def capacity(self):
        """
        This gets the battery amount remaining.
        :return:
        """
        battery_curve = [
            [4.16, 5.5, 100, 100],
            [4.05, 4.16, 87.5, 100],
            [4.00, 4.05, 75, 87.5],
            [3.92, 4.00, 62.5, 75],
            [3.86, 3.92, 50, 62.5],
            [3.79, 3.86, 37.5, 50],
            [3.66, 3.79, 25, 37.5],
            [3.52, 3.66, 12.5, 25],
            [3.49, 3.52, 6.2, 12.5],
            [3.1, 3.49, 0, 6.2],
            [0, 3.1, 0, 0],
        ]
        self.BATTERY_LEVEL = 0
        battery_v, self.CHARGING = self.voltage()
        for r in battery_curve:
            if r[0] < battery_v <= r[1]:
                level_base = np.multiply(
                    np.divide(
                        np.subtract(battery_v, r[0]),
                        np.subtract(r[1], r[0])
                    ),
                    np.subtract(r[3], r[2])
                )
                batt_lvl = np.add(level_base, r[2])
                self.BATTERY_LEVEL = self.reserve(batt_lvl)
        if self.CHARGING:
            self.BATTERY_LEVEL = 'CRG'
        return self.BATTERY_LEVEL

    def battery_gpio_set(self):
        """
        Configured our GPIO registers.
                https://yadi.sk/i/dRp0HTF4oPCo2g

        TODO: It's come to my understanding that these lunatics are multiplexing the GPIOs on the board. /
                This makes the task of getting data a particualr nightmare... /
                The end result is we are going to have to figure out what these things do and how to run them /
                in the proper order... /
                This is also the reason that the data we get from the unit only works some of the time.

        191
        191
        191
        16
        20
        20
        20
        0
        16
        16
        16


        REGISTER: NAME: VALUE: ACTION
        0x26: CHG_DIG_CTL4: 1: VSET PIN: 0: (Can't tell... Default seems to be 191)
        ox52: VSET_sel: 01: GPIO4 (No idea but I think its reset selection, )
        0x53: GPIO4_INEN: 0: disable: 1: enable (GPIO4 input toggle)
        0x54: GPIO4_OUTEN: 0: disable: 1: enable (GPIO output toggle)
        0x55: GPIO4_DAT: (GPIO4 data output pin)


        :return:
        """

    def read_battery_gpio(self):
        """
        Read our GPIO (button / battery) events.
        :return:
        """
        t = self._bus.read_byte_data(self.BAT_ADDRESS, self.CHARGING_REGISTER)
        if not t:
            self.CHARGING = False
        else:
            self.CHARGING = True
        return t
