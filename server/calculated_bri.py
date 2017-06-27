#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Xin Wang

import os
FILE_NAME = 'calculated_brightness.txt'

def write(value, weight=1.0):
    value = float(value)
    old_value = load()
    if old_value == 0:
        new_value = value
    else:
        new_value = (old_value + value * weight) / 2.0
    with open(FILE_NAME, 'w') as fp:
        fp.write(str(new_value))
    return float(new_value)

def load():
    if not os.path.exists(FILE_NAME):
        reset()
        return 0
    with open(FILE_NAME, 'r') as fp:
        value = fp.read()
        if len(value) == 0:
            return 0
    return float(value)

def reset():
    with open(FILE_NAME, 'w') as fp:
        fp.write('')


if __name__ == '__main__':
    write(100, 1) # 100
    print load()
    write(200, 2) # (100+200*2) / 2 = 250
    print load()
    write(50)  # (250 + 50) / 2 = 150
    print load()
    reset()