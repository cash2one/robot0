# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import time
import sys

try:
    import RPi.GPIO as GPIO
except:
    print >> sys.stderr, 'This machine do not support GPIO. Switch to simulator mode.'
    import device.simulator_gpio as GPIO

class SingleMotor:
    Clockwise, InterClockwise = range(2)

    def __init__(self, enb, out, enable_value=True):
        if len(enb) != 2:
            print >> sys.stderr, 'ENB_PIN is not two output(s).'
        if len(out) != 2:
            print >> sys.stderr, 'OUT_PIN is not two output(s).'

        GPIO.setmode(GPIO.BCM)
        self.__enb = enb
        self.__out = out

        # Set all pins as output
        for pin in self.__enb:
            GPIO.setup(pin,GPIO.OUT)
            # set default enable_value
            GPIO.output(pin, enable_value)

        for pin in self.__out:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

    def start(self, direction=Clockwise):
        if direction == SingleMotor.Clockwise:
            GPIO.output(self.__out[0], True)
            GPIO.output(self.__out[1], False)
        else:
            GPIO.output(self.__out[0], False)
            GPIO.output(self.__out[1], True)

    def stop(self):
        GPIO.output(self.__out[0], False)
        GPIO.output(self.__out[1], False)

    def run(self, second, direction=Clockwise):
        self.start(direction)
        time.sleep(second)
        self.stop()

if __name__ == '__main__':
    s = SingleMotor()
    s.run( 
        second = 10,
        direction = SingleMotor.Clockwise
        )




