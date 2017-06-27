#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Xin Wang
import os
import json
STATE_FILE = 'state.json'

def loads():
    if os.path.exists(STATE_FILE):
        return json.loads(open(STATE_FILE, 'r').read())
    else:
        data = {'motor_dir': '', 'motor_running': False, 'light': False, 'bri': 0, 'curtain': ''}
        with open(STATE_FILE, 'w') as fp:
            fp.write(json.dumps(data))
        return data

def save(data):
    with open(STATE_FILE, 'w') as fp:
        fp.write(json.dumps(data))

def main():
    pass

if __name__ == '__main__':
    main()