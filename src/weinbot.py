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
objs = [alarm, brushes, conveyor, drive, path, pump]
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
    """
        poweroff: poweroff the BBB.

    """
    shutoff.shutdown(1)
    subprocess.call("poweroff")

def reboot():
    """
        reboot: poweroff the BBB.

    """
    shutoff.shutdown()
    subprocess.call("reboot")

def operation_start(objects):
    """
        operation_start: call start methods for objects.

    """
    for obj in objects:
        obj.start()

def operation_stop(objects):
    """
        operation_start: call stop methods for objects.

    """
    for obj in objects:
        obj.stop()

def dummy():
    """
        dummy: dummy function that does nothing.

    """
    pass

# Command mapping.
wet = (alarm, brushes, conveyor)
dry = (alarm, brushes, conveyor, pump)

dispatcher = {
        """
            element0: -1 utility, 0 reset, 1 demonstrate
            For demonstration commands:
                element1: type
                element2: parameter
                element3: operation level

            Implemented demos:
                Straight forward at 1m/s for 3 seconds (none, brushes, brushes+pump).
                Straight forward at 0.3m/s for 9 seconds (none, brushes, brushes+pump).
                Left turn forward of r=10m at 0.3m/s for 9 seconds (none, brushes, brushes+pump).
                Left turn forward of r=5m at 0.3m/s for 9 seconds (none, brushes, brushes+pump).
                Left turn forward of r=2m at 0.3m/s for 3 seconds (none).
                Left turn forward of r=0.9m at 45deg/s for 2 seconds (none).
                Left square forward of l=4m at 0.6m/s, 1 corner (none, brushes, brushes+pump).
                Left square forward of l=4m at 0.6m/s, 4 corners (none, brushes, brushes+pump).
        """
        (-1, -1, -1, -1): reboot,
        (-1, 1, -1, 1): poweroff,
        (-1, 1, 1, 1): lambda: operation_start(wet),
        (-1, 0, 0, 0): lambda: operation_stop(wet),
        (1, 1, 1, -1): lambda: path.path(demos.straight_fwd(1, 3), lambda: dummy, lambda: dummy),
        (1, 1, 1, 0): lambda: path.path(demos.straight_fwd(1, 3), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, 1, 1, 1): lambda: path.path(demos.straight_fwd(1, 3), lambda: operation_start(wet), lambda: operation_stop(wet)),
        (1, 1, 0, -1): lambda: path.path(demos.straight_fwd(0.3, 9), lambda: dummy, lambda: dummy),
        (1, 1, 0, 0): lambda: path.path(demos.straight_fwd(0.3, 9), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, 1, 0, 1): lambda: path.path(demos.straight_fwd(0.3, 9), lambda: operation_start(wet), lambda: operation_stop(wet)),
        (1, 1, -1, -1): lambda: path.path(demos.turn_fwd(0.3, "left", 10, 9), lambda: dummy, lambda: dummy),
        (1, 1, -1, 0): lambda: path.path(demos.turn_fwd(0.3, "left", 10, 9), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, 1, -1, 1): lambda: path.path(demos.turn_fwd(0.3, "left", 10, 9), lambda: operation_start(wet), lambda: operation_stop(wet)),
        (1, 0, 1, -1): lambda: path.path(demos.turn_fwd(0.3, "left", 5, 9), lambda: dummy, lambda: dummy),
        (1, 0, 1, 0): lambda: path.path(demos.turn_fwd(0.3, "left", 5, 9), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, 0, 1, 1): lambda: path.path(demos.turn_fwd(0.3, "left", 5, 9), lambda: operation_start(wet), lambda: operation_stop(wet)),
        (1, 0, 0, -1): lambda: path.path(demos.turn_fwd(0.3, "left", 2, 3), lambda: dummy, lambda: dummy),
        (1, 0, 0, 0): lambda: path.path(demos.turn_fwd(45, "left", 0.9, 2), lambda: dummy, lambda: dummy),
        (1, -1, 0, -1): lambda: path.path(demos.square(0.6, "left", 4, corners=1), lambda: dummy, lambda: dummy),
        (1, -1, 0, 0): lambda: path.path(demos.square(0.6, "left", 4, corners=1), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, -1, 0, 1): lambda: path.path(demos.square(0.6, "left", 4, corners=1), lambda: operation_start(wet), lambda: operation_stop(wet)),
        (1, -1, 1, -1): lambda: path.path(demos.square(0.6, "left", 4, corners=4), lambda: dummy, dummy),
        (1, -1, 1, 0): lambda: path.path(demos.square(0.6, "left", 4, corners=4), lambda: operation_start(dry), lambda: operation_stop(dry)),
        (1, -1, 1, 1): lambda: path.path(demos.square(0.6, "left", 4, corners=4), lambda: operation_start(wet), lambda: operation_stop(wet)),
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


