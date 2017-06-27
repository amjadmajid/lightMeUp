#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import sys
import RPi.GPIO as GPIO

from daemon import runner
MAX_CYCLE = 22000

class Motor():


    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/motor_daemon.pid'
        self.pidfile_timeout = 5

        self.pins = [7, 11, 13, 15]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        for pin in self.pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)


    def run(self):
        wait_time = 0.001
        # default value: cw
        clockwise = 1
        # you can use `./motor_daemon.py start 0` to make it ccw
        if len(sys.argv) > 2:
            clockwise = int(sys.argv[2])
        phases = 8
        step_counter = 0
        seq = []
        seq = range(0, phases)
        if clockwise:
            seq[0] = [1,0,0,0]
            seq[1] = [1,1,0,0]
            seq[2] = [0,1,0,0]
            seq[3] = [0,1,1,0]
            seq[4] = [0,0,1,0]
            seq[5] = [0,0,1,1]
            seq[6] = [0,0,0,1]
            seq[7] = [1,0,0,1]
        else:
            seq[0] = [1,0,0,1]
            seq[1] = [0,0,0,1]
            seq[2] = [0,0,1,1]
            seq[3] = [0,0,1,0]
            seq[4] = [0,1,1,0]
            seq[5] = [0,1,0,0]
            seq[6] = [1,1,0,0]
            seq[7] = [1,0,0,0]

        cycle = 0
        # Start main loop
        while 1:
            for pin in range(0, 4):
                xpin = self.pins[pin]
                if seq[step_counter][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            step_counter += 1
            if step_counter == phases:
                step_counter = 0
            cycle += 1
            if cycle == MAX_CYCLE:
                break

            time.sleep(wait_time)

print 'Usage: ./motor_daemon.py start [wise]'
app = Motor()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()