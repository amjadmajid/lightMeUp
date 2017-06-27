#!/usr/bin/env python

from flask import Flask, request
from utils import render_json, is_night, log_data
import os
import time
import subprocess

import motor
import calculated_bri
import device_state
import curtain
import hue

app = Flask(__name__)

THRESHOLD = 10.0
MAX_LIGHT = 255
MIN_LIGHT = 0
LIGHT_STEP = 20
CURTAIN_MAX = 40
CURTAIN_MIN = 3

@app.route('/')
def hello():
    return render_json('hello')


@app.route('/quit')
def quit():
    motor.stop()
    state = device_state.loads()
    state['motor_running'] = False
    # hue.set_light(False, bri=0)
    calculated_bri.reset()
    return render_json(state)

# Control
@app.route('/control')
def control():
    try:
        desired = float(request.args.get('desired'))
        current = float(request.args.get('current'))
        weight  = float(request.args.get('weight'))
    except Exception as e:
        print e
        return u'Invalid parameters'

    state = device_state.loads()
    print '-' * 80
    print state
    print '-' * 80
    desired = calculated_bri.write(desired, weight)
    diff = desired - current
    print '>> current: %d, desired: %d, diff: %d' % (current, desired, diff)
    log_data(current, desired)

    # if is_night():
    if 0:
        print '>> nighttime'

        # curtain is still open
        if current > THRESHOLD and not curtain.is_closed():
            # hue.set_light(False, bri=0)
            print '>> curtain is still open'
            motor.run_ccw()
            print '>> night: motor down'
            state['motor_running'] = True
            state['motor_dir'] = 'down'
            state['curtain'] = 'closed'
            curtain.set_closed()
            # if current < CURTAIN_MIN:
            #     motor.stop()
            #     curtain.set_closed()
            #     state['curtain'] = 'closed'
            #     state['motor_running'] = False
            #     state['motor_dir'] = ''
        # curtain is closed
        else:
            print '>> curtain is closed'
            light_state = hue.get_light()
            if light_state['on']:
                current_light = light_state['bri']
                print '>> bri: %d' % (current_light)
                bri = hue.change(diff, current_light)
            else:
                bri = MAX_LIGHT / 4
            hue.set_light(True, bri=bri)
            state['light'] = True
            state['bri'] = bri
        return render_json(state)

    else:
        print '>> daytime'
        # if curtain is open, but still needs light
        if curtain.is_open():
            print '>> fully open'
            light_state = hue.get_light()
            # if light is on
            if light_state['on']:
                current_light = light_state['bri']
                bri = hue.change(diff, current_light)
                # closes curtain
                if bri == 0:
                    print '>> bri: 0, turn off light'
                    hue.set_light(False, bri=bri)
                    state['light'] = False
                    state['bri'] = bri
                    motor.run_ccw()
                    state['motor_running'] = True
                    state['motor_dir'] = 'down'
                    state['curtain'] = ''
                    curtain.clear_open()
                    return render_json(state)

            else:
                bri = MAX_LIGHT / 2
            hue.set_light(True, bri=bri)
            state['light'] = True
            state['bri'] = bri
            print '>> bri: ', bri
            return render_json(state)

        # if curtain is not fully open
        else:
            print '>> not fully open'
            hue.set_light(False, bri=0)
            state['light'] = False
            state['bri'] = 0
            # if needs motor up (more light): desired > current
            if diff > 0 and abs(diff) > THRESHOLD:
                current = int(current)
                # previous_max = curtain.log_max(current)
                # # if brightness does not increase, we assume the curtain fully open
                # if previous_max - current_int < THRESHOLD:
                #     curtain.set_open()

                # if curtain is opening
                if state['motor_dir'] != 'down' and current > CURTAIN_MAX:
                    curtain.set_open()
                    motor.stop()
                    state['curtain'] = 'open'
                    state['motor_running'] = False
                    state['motor_dir'] = ''
                else:
                    motor.run_cw()
                    print '>> motor up'
                    state['motor_dir'] = 'up'
                    state['motor_running'] = True
                    state['curtain'] = ''
                    curtain.clear_closed()
                return render_json(state)
            # if needs motor down
            if diff < 0 and abs(diff) > THRESHOLD:
                print '>> motor down'
                motor.run_ccw()
                state['motor_dir'] = 'down'
                state['motor_running'] = True
                curtain.clear_open()
                state['curtain'] = ''
                # if no light, set curtain state as closed
                if not state['light'] and current < CURTAIN_MIN:
                    motor.stop()
                    curtain.set_closed()
                    state['curtain'] = 'closed'
                    state['motor_running'] = False
                    state['motor_dir'] = ''
                return render_json(state)
            # stops the motor
            else:
                motor.stop()
                state['motor_running'] = False
                state['motor_dir'] = ''
                if current < CURTAIN_MIN:
                    state['curtain'] = 'closed'
                return render_json(state)



# up
@app.route('/motor/start/cw')
def motor_start_cw():
    motor.run_cw()
    state = device_state.loads()
    state['motor_running'] = True
    state['motor_dir'] = 'up'
    return render_json(state)

# down
@app.route('/motor/start/ccw')
def motor_start_ccw():
    motor.run_ccw()
    state = device_state.loads()
    state['motor_running'] = True
    state['motor_dir'] = 'down'
    return render_json(state)

@app.route('/control/stop')
def control_stop():
    try:
        desired = float(request.args.get('desired'))
        current = float(request.args.get('current'))
        weight  = float(request.args.get('weight'))
        desired = calculated_bri.write(desired, weight)
        diff = desired - current
        print '>> current: %d, desired: %d, diff: %d' % (current, desired, diff)
        log_data(current, desired)
    except Exception as e:
        print e


    state = device_state.loads()
    state['motor_running'] = False
    motor.stop()
    return render_json(state)

# Lights
@app.route('/lights/on/<int:light_id>')
def lights_on(light_id):
    hue.set_light(True, light_id)
    return render_json({'light': light_id, 'state': 'on'}, code=201)

@app.route('/lights/off/<int:light_id>')
def lights_off(light_id):
    hue.set_light(False, light_id)
    return render_json({'light': light_id, 'state': 'off'}, code=201)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)