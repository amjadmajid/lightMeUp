#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Xin Wang
# @Date:   2014-10-10 16:07:13

from flask import Response
from datetime import datetime
import json
import time
import device_state

def render_json(result, code=200):
    if code == 200:
        device_state.save(result)
    results = {'code': code, 'results': result}
    r = Response()
    r.response = json.dumps(results)
    r.mimetype = 'application/json'
    r.headers['X-LightMeUp'] = 'v1.0'
    return r

def is_night():
    # night time: 18:00 - 06:00
    now = datetime.now()
    if now.hour > 18:
        return True
    if 0 <= now.hour < 8:
        return True
    return False


def log_data(current, desired):
    with open('lux_data.txt', 'a') as fp:
        fp.write('%d\t%d\t%d\n' % (int(time.time()), int(current), int(desired)))