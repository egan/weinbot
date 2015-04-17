##
# Brushes.py: Class implementing control of WEINBot brush motor relay via
#             GPIO.
#
# Copyright 2015, Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class Brushes():
    """
        Brushes: A class that provides an interface to control the WEINBot
                 brush motor relay via GPIO.
    """

    def __init__(self, pin="P8_11"):
        """
            pin: BBB GPIO pin to control brush motor relay.

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
            start: Start the brush motors.

        """
        logging.debug("brushes: started")
        GPIO.output(self.pin, GPIO.HIGH)

    def stop(self):
        """
            stop: Stop the brush motors.

        """
        logging.debug("brushes: stopped")
        GPIO.output(self.pin, GPIO.LOW)
