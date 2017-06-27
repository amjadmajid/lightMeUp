#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Xin Wang

import requests
import json
BASE_ADDR = 'http://192.168.2.100/api/newdeveloper'

DEFAULT_LIGHT = 3
LIGHT_STEP = 20
LIGHT_MAX = 255

def set_light(state, **kwargs):
    payload = {'on': state, 'sat': 100, 'hue': 42029}
    payload = dict(payload.items() + kwargs.items())
    try:
        url = '%s/lights/%d/state' % (BASE_ADDR, DEFAULT_LIGHT)
        # print url
        r = requests.put(url, json.dumps(payload))
        return r.text
    except Exception, e:
        print 'set_light error: ', e
        return None

def get_light():
    try:
        url = '%s/lights/%d' % (BASE_ADDR, DEFAULT_LIGHT)
        r = requests.get(url)
        result = json.loads(r.text)
        # print result
        return result['state']
    except Exception, e:
        print 'get_light error: ', e
        return None

def change(diff, current_light):
    if abs(diff) < 30:
        return current_light
    if diff > 0:
        # more light
        if current_light > LIGHT_MAX - LIGHT_STEP:
            current_light = LIGHT_MAX - LIGHT_STEP
        brightness = current_light + LIGHT_STEP
    else:
        # less light
        if current_light < LIGHT_STEP:
            current_light = LIGHT_STEP
        brightness = current_light - LIGHT_STEP
    return brightness

if __name__ == '__main__':
    print set_light(True, bri=90)
    exit()
    import time
    print set_light(True, bri=129) #, bri=64, hue=29012)
    print get_light()
    time.sleep(3)
    print set_light(True, bri=64)
    print get_light()
    time.sleep(3)
    print set_light(True, bri=32)
    print get_light()
    set_light(False)
