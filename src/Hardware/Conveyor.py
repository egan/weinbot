##
# Conveyor.py: Class implementing control of WEINBot conveyor motor relay via
#              GPIO.
#
# Copyright 2015, Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class Conveyor():
    """
        Conveyor: A class that provides an interface to control the WEINBot
                  conveyor motor relay via GPIO.
    """

    def __init__(self, pin="P8_12"):
        """
            pin: BBB GPIO pin to control conveyor motor relay.

        """

        # Set up GPIO.
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        return None

    def __del__(self):
        self.stop()
        return

    def start(self):
        """
            start: Start the conveyor motor.

        """
        logging.debug("conveyor: started")
        GPIO.output(self.pin, GPIO.HIGH)

    def stop(self):
        """
            stop: Stop the conveyor motor.

        """
        logging.debug("conveyor: stopped")
        GPIO.output(self.pin, GPIO.LOW)
