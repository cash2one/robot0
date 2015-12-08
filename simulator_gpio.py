#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 
# This python code simulate the GPIO behavior.
#

import sys

BCM, BOARD, OUT = range(3)
ConstStr = ['BCM', 'BOARD', 'OUT']

def slog(s):
    print >> sys.stderr, '[GPIO_SIMULATOR] : %s' % (s)

def setmode(mode):
    slog('set_mode mode=%d:%s' % ( mode, ConstStr[mode]))

def setup(pin, t):
    slog('setup PIN[%d] value=%d:%s' % (pin, t, ConstStr[t]))

def output(pin, value):
    slog('output PIN[%d] value=%s' % (pin, value))

if __name__=='__main__':
    pass







