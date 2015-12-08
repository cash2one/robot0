# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import sys
import json

try:
    import RPi.GPIO as GPIO
except:
    print >> sys.stderr, 'This machine do not support GPIO. Switch to simulator mode.'
    import simulator_gpio as GPIO

import pydev

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
                print >> sys.stderr, 'Init: %s' % dat['pins']
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

class GPIORemoteClient:
    def __init__(self, server_ip, server_port):
        self.__ip = server_ip
        self.__port = server_port

    def init(self, out_pins):
        d = {'cmd':'init', 'pins':out_pins}
        ret = pydev.simple_query(query=json.dumps(d), ip=self.__ip, port=self.__port)
        print >> sys.stderr, 'Return = %s' % ret
        return ret

    def set(self, pins, value=True):
        d = {'cmd':'set', 'pins':pins, 'value':value}
        ret = pydev.simple_query(query=json.dumps(d), ip=self.__ip, port=self.__port)
        print >> sys.stderr, 'Return = %s' % ret
        return ret

    def batch(self, pin_values):
        d = {'cmd':'batch', 'kv':pin_values}
        ret = pydev.simple_query(query=json.dumps(d), ip=self.__ip, port=self.__port)
        print >> sys.stderr, 'Return = %s' % ret
        return ret

    def execute(self, query):
        cmd = query.split(' ')
        if cmd[0] == 'init':
            self.init(map(lambda x:int(x), cmd[1].split(',')))
        elif cmd[0] == 'set':
            if len(cmd) == 3:
                self.set( map(lambda x:int(x), cmd[1].split(',')), int(cmd[2]) )
            else:
                self.set( map(lambda x:int(x), cmd[1].split(',')) )
        elif cmd[0] == 'batch':
            d = dict(map(lambda x:map(lambda x:int(x), x.split(':')), cmd[1:]))
            self.batch(d)
        else:
            print >> sys.stderr, 'Cannot recognize query=[%s]' % query

if __name__ == '__main__':
    if len(sys.argv)!=4:
        print >> sys.stderr, 'Usage : easy_gpio.py [server|client] <ip> <port>'
        sys.exit(-1)

    mode, ip, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if mode == 'server':
        print >> sys.stderr, 'GPIORemoteServer at %s:%d' % (ip, port)

        gpio_server = GPIORemoteServer()
        s = pydev.BasicService()
        s.set_process(gpio_server.process)
        s.run(ip, port)

    elif mode == 'client':
        gpio_client = GPIORemoteClient(ip, port)
        while 1:
            cmd = sys.stdin.readline()
            if cmd == '':
                break
            gpio_client.execute(cmd)


