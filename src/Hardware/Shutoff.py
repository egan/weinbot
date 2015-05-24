##
# Shutoff.py: Class implementing procedure in response to emergency shutoff
#             switch.
#
# Copyright 2015, Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class Shutoff():
    """
        Shutoff: A class implementing shutdown procedures upon receiving rising
                 edge interrupt on GPIO from NO pole of emergency shutoff
                 switch or sensing edges.
    """

    def __init__(self, pin, objects=[]):
        """
            pin:       GPIO pin on which to wait for rising edge.
            objects:   list of objects to call stop() methods for.

        """
        self.pin = pin
        self.objects = objects

        # Set up GPIO interrupt on rising edge.
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.__handler, bouncetime=500)
        return None

    def __del__(self):
        self.shutdown()
        return

    def __handler(self, channel):
        """
                channel: required argument for callback, unused.

        """
        if GPIO.input(self.pin):
            self.shutdown()
            logging.debug("shutoff: waiting for reset")
            while GPIO.input(self.pin):
                pass
        else:
            logging.debug("shutoff: switch reset")

        return

    def shutdown(self):
        """
            shutdown: Call stop() methods for shutoff objects.

        """
        # Shut down Hardware objects.
        logging.debug("shutoff: shutdown event received")
        for obj in self.objects:
            obj.stop()

        return

