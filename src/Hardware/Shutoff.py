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

    def __init__(self, pin="P9_41", gpio_mode, objects=[]):
        """
            pin:       GPIO pin on which to wait for rising edge.
            gpio_mode: type of edge to trigger, reset
            objects:   list of objects to call stop() methods for.

        """
        self.pin = pin
        self.gpio_mode = gpio_mode
        self.objects = objects

        # Set up GPIO interrupt on rising edge.
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, gpio_mode[0], callback=self.shutdown, bouncetime=500)
        return None

    def __del__(self):
        self.shutdown()
        return

    def shutdown(self, channel):
        """
            shutdown: Call stop() methods for shutoff objects.

                channel: required argument for callback, unused.

        """
        # Shut down Hardware objects.
        logging.debug("shutoff: shutdown interrupt received")
        for obj in self.objects:
            obj.stop()
        # XXX: Other shutdown tasks.

        # Wait until switch is reset.
        logging.debug("shutoff: waiting for reset")
        GPIO.wait_for_edge(self.pin, gpio_mode[1])
        return
