# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import RPi.GPIO as GPIO
import sys
import pydev
import json

class SimpleGPIO:
    def __init__(self, out_pins, mode=GPIO.BCM):
        GPIO.setmode(mode)
        self.__pins = []
        for pin in out_pins:
            self.__pins.append(pin)
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

    def reset(self, value=False):
        for pin in self.__pins:
            GPIO.output(pin, value)

    def set(self, pins, value=True):
        for pin in pins:
            print >> sys.stderr, 'Set [%d] to [%s]' % (pin, str(value))
            GPIO.output(pin, value)

    def batch(self, pin_values):
        if isinstance(pin_values, dict):
            for pin, value in pin_values.iteritems():
                pin = int(pin)
                if value:
                    GPIO.output(pin, True)
                else:
                    GPIO.output(pin, False)
        else:
            for pin, value in pin_values:
                pin = int(pin)
                if value:
                    GPIO.output(pin, True)
                else:
                    GPIO.output(pin, False)

class GPIORemoteServer:
    def __init__(self):
        self.__gpio = None

    def process(self, query):
        try:
            dat = json.loads(query)
            print >> sys.stderr, 'Keys: %s' % (dat.keys())
            cmd = dat['cmd']

            if cmd == 'init':
                print >> sys.stderr, 'Init: [%s]' % dat['pins']
                self.__gpio = SimpleGPIO(dat['pins'])

            elif cmd == 'set':
                print >> sys.stderr, 'Set: [%s]' % dat['pins']
                v = True
                if 'value' in dat:
                    v = dat['value']
                    print >> sys.stderr, 'Set_value: [%d]' % (dat['value'])
                self.__gpio.set(dat['pins'], v)

            elif cmd == 'batch':
                print >> sys.stderr, 'Batch: %s' % dat['kv']
                self.__gpio.batch(dat['kv'])
            return '0,OK'

        except Exception, ex:
            return '-1,%s' % (str(ex))

class GPIORemoveClient:
    def __init__(self, server_ip, server_port):
        pass

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print >> sys.stderr, 'Usage : easy_gpio.py <ip> <port>'
        sys.exit(-1)

    ip, port = sys.argv[1], int(sys.argv[2])
    print >> sys.stderr, 'GPIORemoteServer at %s:%d' % (ip, port)

    gpio_server = GPIORemoteServer()
    s = pydev.BasicService()
    s.set_process(gpio_server.process)
    s.run(ip, port)



