#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Xin Wang
import os

def set_open():
    open('curtain_open.lock', 'a')
    if os.path.exists('curtain_closed.lock'):
        os.remove('curtain_closed.lock')

def set_closed():
    open('curtain_closed.lock', 'a')
    if os.path.exists('curtain_open.lock'):
        os.remove('curtain_open.lock')

def clear_closed():
    if os.path.exists('curtain_closed.lock'):
        os.remove('curtain_closed.lock')

def clear_open():
    if os.path.exists('curtain_open.lock'):
        os.remove('curtain_open.lock')

def is_closed():
    return os.path.exists('curtain_closed.lock')

def is_open():
    return os.path.exists('curtain_open.lock')

def log_max(value):
    filename = 'curtain_max.txt'
    if not os.path.exists(filename):
        with open(filename, 'w') as fp:
            fp.write('0')
        return 0
    with open(filename, 'r+') as fp:
        old_value = int(fp.read())
        max_value = max(value, old_value)
        fp.seek(0)
        fp.write('%d' % (max_value))
        return max_value

def clear_max():
    os.remove('curtain_max.txt')


def main():
    pass

if __name__ == '__main__':
    main()