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
        Shutoff: A class implementing shutdown procedures upon receiving
                 shutdown interrupt on GPIO from NO pole of emergency shutoff
                 switch.
    """

    def __init__(self, pin="P9_41", objects=[]):
        """
            pin:      GPIO pin on which to wait for rising edge.
            objects:  list of objects to call stop() methods for.

        """
        self.objects = objects

        # Set up GPIO interrupt on rising edge.
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.shutdown, bouncetime=300)
        return None

    def __del__(self):
        self.shutdown()
        return

    def shutdown():
        """
            shutdown: Call stop() methods for shutoff objects.

        """
        logging.debug("shutoff: shutdown interrupt received")
        for obj in self.objects:
            obj.stop()

        return
