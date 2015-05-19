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
measure_waste = False
waste_critical = 0.5
waste_samples = 3
waste_counter = 0

## Initialization.
# Instantiate hardware objects. See available init() arguments in respective docstrings.
alarm = Alarm()
brushes = Brushes()
conveyor = Conveyor()
drive = Drive()
loadcell = LoadCell()
hmi = HMI()
pump = Pump()

# Instantiate control objects.
path = Path(drive)
objs = [alarm, brushes, conveyor, drive, pump]
shutoff = Shutoff(objects=objs)
sensing = Shutoff(pin="P9_3", objects=objs)

# Instantiate sensor objects.
imu = IMU()

# Utility functions.
def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def exit_handler():
    imu.go = False
    GPIO.cleanup()

    logging.debug("WEINBot control software exiting")
    sys.exit

atexit.register(exit_handler)

def poweroff():
    shutoff.shutdown(1)
    subprocess.call("poweroff")

def reboot():
    shutoff.shutdown()
    subprocess.call("reboot")

# Command mapping.
dispatcher = {
        (-1, -1, -1, -1): reboot,
        (-1, 1, -1, 1): poweroff,
        }

## Run.
# Signal control software ready.
alarm.strobe(1, (0.4, 0.2, 0.4, 0.2, 0.4))

# Mode selection loop (only in non-interactive mode).
if not run_from_ipython():
    while True:
        if measure_waste:
            if loadcell.read() > waste_critical:
                counter += 1
            else:
                counter = 0

            if counter >= waste_samples:
                # XXX: Waste is full, stop and alert.
                pass

        command = hmi.read()
        if command in dispatcher.keys():
            dispatcher[command]()
        elif command is not None:
            logging.debug("mos: unmapped command %s" %(repr(command)))
        else:
            pass
else:
        logging.debug("WEINBot control software ready for interaction")


