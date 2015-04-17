##
# Brushes.py: Class implementing control of WEINBot brush motor relay via
#             GPIO.
#
# Copyright 2015, Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO

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

    def start():
        """
            start: Start the brush motors.

        """
        GPIO.output(self.pin, GPIO.HIGH)

    def stop():
        """
            stop: Stop the brush motors.

        """
        GPIO.output(self.pin, GPIO.LOW)
