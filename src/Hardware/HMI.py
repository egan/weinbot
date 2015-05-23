##
# HMI.py: Class implementing reading of HMI SPDT toggle array.
#
# Copyright 2015, Natalie Pueyo Svoboda
#                 Egan McComb
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class HMI():
    """
        HMI: A class that provides an interface to read the HMI SPDT toggle switches.

    """

    def __init__(self, pins=(("P8_37", "P8_38"), ("P8_39", "P8_40"), ("P8_41", "P8_42"), ("P8_43", "P8_44")), trigger=1):
        """
            pins:    tuple of tuples of GPIO pins corresponding to toggle
                     switch and its states (low, high).
            trigger: Switch number that acts as the command trigger.

        """

        # Set up GPIO.
        self.pins = pins
        for switch in pins:
            for pin in switch:
                GPIO.setup(pin, GPIO.IN)

        self.trigger = trigger-1
        self.lock = False

        return None

    def __switchState(self, switch):
        """
            switchState: Return balanced ternary switch state.

                switch: Tuple of switch pins (low, high).

        """
        if GPIO.input(switch[0]):
            # Check for circuitry fault.
            if GPIO.input(switch[1]):
                # Impossible state.
                logging.error("hmi: impossible state detected on %s" %(switch[0]+ ',' + switch[1]))
                return None
            # Switch is low.
            return -1
        elif GPIO.input(switch[1]):
            # Switch is high.
            return 1
        else:
            # Switch is neutral.
            return 0

    def read(self):
        """
            read: Return numeric identifier of toggle switch state. This method
                  is meant to be run in a continuous loop and so should be tested
                  carefully.

        """
        # Determine state of every switch.
        state=[]
        for switch in self.pins:
            state.append(self.__switchState(switch))

        if None in state:
            # Impossible state: void reading.
            return

        if state[self.trigger] == 0:
            # Trigger not active, skip.
            if self.lock:
                logging.debug("hmi: resetting lock")
                self.lock = False
            return
        elif self.lock:
            # Trigger not reset, skip!
            # logging.debug("hmi: waiting for trigger reset")
            return
        else:
            # Trigger active: set lock and return state.
            logging.debug("hmi: state read")
            self.lock = True
            return tuple(state)

