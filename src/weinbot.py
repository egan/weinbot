##
# weinbot.py: Master program for WEINBot.
#
# Copyright 2015, Egan McComb
#
##

## External libraries and modules.
from __future__ import division
import atexit
import logging
import time
import Adafruit_BBIO.GPIO as GPIO

## In-house libraries and modules.
from Drive.Drive import Drive as Drive
from Hardware import *
from Navigate.Path.Path import Path

## Logging.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("WEINBot control software launching %s" %(time.strftime("%a, %D %T")))

## Parameters.
deadman = "P9_42"

## Initialization.
# Instantiate hardware objects.
alarm = Alarm()
brushes = Brushes()
drive = Drive()
pump = Pump()
shutoff = Shutoff(objects=[alarm, brushes, drive, pump])

# Deadman's switch handling.
GPIO.setup(deadman, GPIO.OUT)

def exit_handler():
    GPIO.cleanup()
    GPIO.output(deadman, GPIO.LOW)
    logging.debug("WEINBot control software exiting")

atexit.register(exit_handler)
GPIO.output(deadman, GPIO.HIGH)

## Run.
path_spec = [("fwd", 1, "right", 2, 10)]
path = Path(drive, path_spec)
