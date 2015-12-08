# -*- coding: utf-8 -*-
# gusimiu@baidu.com
# 

import time
import RPi.GPIO as GPIO
import sys

class StepMotor:
    Clockwise, InterClockwise = range(2)
    Fast, Normal, Slow = (0.002, 0.005, 0.01)

    def __init__(self, step_pins=(17, 18, 27, 22), unit_amount=130):
        # GPIO.setmode(GPIO.BCM)
        self.__step_pins = step_pins
        # Set all pins as output
        for pin in self.__step_pins:
            #print "Setup pins"
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        self.__unit_amount = unit_amount

        self.__cw_seq = (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1),
                )
        self.__icw_seq = (
                (0, 0, 0, 1),
                (0, 0, 1, 0),
                (0, 1, 0, 0),
                (1, 0, 0, 0),
                )


    def run(self, quantity, direction=Clockwise, speed=Normal):
        # Define some settings
        if direction == StepMotor.Clockwise:
            seq = self.__cw_seq
        else:
            seq = self.__icw_seq

        counter = 0
        while 1==1:
            for pin in range(0, 4):
                xpin = self.__step_pins[pin]
                if seq[counter % len(seq)][pin]!=0:
                    #print >> sys.stderr, 'put: %d -> %d' % (pin, xpin)
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

            # Wait before moving on
            time.sleep(speed)
            counter += 1
            if counter / (self.__unit_amount * len(seq)) == quantity:
                break

if __name__ == '__main__':
    s = StepMotor()
    s.run( 
        quantity = 6, 
        direction = StepMotor.InterClockwise,
        speed = StepMotor.Slow
        )
