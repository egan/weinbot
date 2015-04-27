##
# Hardware.py: Class implementing control of WEINBot Human Machine Interface.
#
# Copyright 2015, Natalie Pueyo Svoboda
#
##

import Adafruit_BBIO.GPIO as GPIO
import logging

class HMI():
    """
        HMI: A class that provides an interface to read the HMI switches to 
               select the desired WEINBot demo.
    """

    def __init__(self, pins_selector=("P8_37", "P8_38", "P8_39", "P8_40", "P8_41", "P8_42", "P8_43", "P8_44")):
        """
            pins_selector: BBB GPIO pins to read state of HMI switch array.

        """

        # Set up GPIO.
        self.pins_selector = pins_selector
        for pin in pins_selector:
            GPIO.setup(pin, GPIO.IN)

        return None

    def __del__(self):
        self.stop()
        return

    def HMI_state(self):
        """
            HMI_state: Read GPIO pins to determine what demo will be set.
        """
        state = 0

        # Read GPIO pins to determine the state of each switch
        if GPIO.input(self.pins_selector[0]):
            state = state + 1

        if GPIO.input(self.pins_selector[1]):
            state = state + 2

        if GPIO.input(self.pins_selector[2]):
            state = state + 4

        if GPIO.input(self.pins_selector[3]):
            state = state + 8

        if GPIO.input(self.pins_selector[4]):
            state = state + 16

        if GPIO.input(self.pins_selector[5]):
            state = state + 32

        if GPIO.input(self.pins_selector[6]):
            state = state + 64

        if GPIO.input(self.pins_selector[7]):
            state = state + 128

        return state