# -*- coding: UTF-8 -*-
"""
This file is part of the cvkiosk package.
Copyright (c) 2021 Kevin Eales.
------------------------------------------------------------------------------------------------------------------------

This is full of aptly named test code.
"""
import numpy as np


cup = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]
cdown = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


cup_invalid = list(cup)
cdown_invalid = list(cdown)
limit = 2

for idx, (up, down) in enumerate(zip(cup, cdown)):
    # Create the limit block.
    if idx < limit:
        start = 0
        stop = idx
    else:
        start = np.subtract(idx, limit)
        stop = idx
    # Remove invalids from valid lists.
    if up or down:
        "set both lists [start:stop] to zero"
        block = [0] * int(np.subtract(stop, start))
        cup[start:stop] = block
        cdown[start:stop] = block
        if up and down:
            cup[idx] = cdown[idx] = 0
# Collect the invalidated signals.
pass
for idx, (inval_up, inval_down, val_up, val_down) in enumerate(zip(cup_invalid, cdown_invalid, cup, cdown)):
    if inval_up and val_up:
        cup_invalid[idx] = 0
    if inval_down and val_down:
        cdown_invalid[idx] = 0

pass
