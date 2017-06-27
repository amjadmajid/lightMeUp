#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os

def run_cw():
    FNULL = open(os.devnull, 'w')
    # if running ccw
    if os.path.exists('running_ccw.lock'):
        subprocess.Popen('sudo ./motor_daemon.py stop'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
        os.remove('running_ccw.lock')
    # if running cw
    if os.path.exists('running_cw.lock'):
        return
    subprocess.Popen('sudo ./motor_daemon.py start'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
    open('running_cw.lock', 'a')

def run_ccw():
    FNULL = open(os.devnull, 'w')
    # if running cw
    if os.path.exists('running_cw.lock'):
        subprocess.Popen('sudo ./motor_daemon.py stop'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
        os.remove('running_cw.lock')
    # if running ccw
    if os.path.exists('running_ccw.lock'):
        return
    subprocess.Popen('sudo ./motor_daemon.py start 0'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
    open('running_ccw.lock', 'a')

def stop():
    FNULL = open(os.devnull, 'w')
    if os.path.exists('running_cw.lock'):
        subprocess.Popen('sudo ./motor_daemon.py stop'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
        os.remove('running_cw.lock')
    if os.path.exists('running_ccw.lock'):
        subprocess.Popen('sudo ./motor_daemon.py stop'.split(), stdout=FNULL, stderr=subprocess.STDOUT)
        os.remove('running_ccw.lock')