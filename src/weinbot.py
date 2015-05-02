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
import sys
import time
import Adafruit_BBIO.GPIO as GPIO

## In-house libraries and modules.
from Drive.Drive import Drive as Drive
from Hardware import *
from Sensors import *
from Navigate.Path.Path import Path
import demos

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
conveyor = Conveyor()
drive = Drive()
pump = Pump()

# Instantiate control objects.
path = Path(drive)
shutoff = Shutoff(objects=[alarm, brushes, conveyor, drive, pump])

# Instantiate sensor objects.
imu = IMU()

# Deadman's switch handling.
GPIO.setup(deadman, GPIO.OUT)

def exit_handler():
    imu.go = False
    GPIO.cleanup()

    logging.debug("WEINBot control software exiting")
    sys.exit

atexit.register(exit_handler)
GPIO.output(deadman, GPIO.HIGH)

## Run.
# Signal control software ready.
alarm.strobe(1, (0.4, 0.2, 0.4, 0.2, 0.4))
