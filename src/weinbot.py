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
import subprocess
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

## Initialization.
# Instantiate hardware objects. See available init() arguments in respective docstrings.
alarm = Alarm()
brushes = Brushes()
conveyor = Conveyor()
drive = Drive()
hmi = HMI()
pump = Pump()

# Instantiate control objects.
path = Path(drive)
shutoff = Shutoff(objects=[alarm, brushes, conveyor, drive, pump])

# Instantiate sensor objects.
imu = IMU()

# Utility functions.
def exit_handler():
    imu.go = False
    GPIO.cleanup()

    logging.debug("WEINBot control software exiting")
    sys.exit

atexit.register(exit_handler)

def poweroff():
    shutoff.shutdown()
    subprocess.call("poweroff")

def reboot():
    shutoff.shutdown()
    subprocess.call("reboot")

## Run.
# Signal control software ready.
alarm.strobe(1, (0.4, 0.2, 0.4, 0.2, 0.4))

# Mode selection loop.
