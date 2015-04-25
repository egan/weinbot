##
# Pump.py: Class implementing control of WEINBot water pump via GPIO.
#
# Copyright 2015, Natalie Pueyo Svoboda
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class Pump():
    """
        Pump: A class that provides an interface to control the WEINBot
                 water pump via GPIO.
    """

    def __init__(self, pin="P8_13"):
        """
            pin: BBB GPIO pin to control the water pump.

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
            start: Start the pump.

        """
        logging.debug("pump: started")
        GPIO.output(self.pin, GPIO.HIGH)

    def stop(self):
        """
            stop: Stop the pump.

        """
        logging.debug("pump: stopped")
        GPIO.output(self.pin, GPIO.LOW)
