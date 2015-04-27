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

    # Dictionary set with functiI switch array configuration up to 16
    setHMI = {
        0 : default_state,
        1 : demo_1,
        2 : demo_2,
        3 : demo_3,
        4 : demo_4,
        5 : demo_5,
        6 : demo_6,
        7 : demo_7,
        8 : demo_8,
        9 : demo_9,
        10 : demo_10,
        11 : demo_11,
        12 : demo_12,
        13 : demo_13,
        14 : demo_14,
        15 : demo_15,
        }

    def __init__(self, pins_selector=("P8_37", "P8_38", "P8_39", "P8_40", "P8_41", "P8_42", "P8_43", "P8_44")):
        """
            pins_selector: BBB GPIO pins to read state of HMI switch array.

        """

        # Set up GPIO.
        self.pin_enable = pin_enable
        GPIO.setup(pin_enable, GPIO.IN)
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

        # Add once we know more than 16 states are needed
        #if GPIO.input(self.pins_selector[4]):
        #    state = state + 16

        #if GPIO.input(self.pins_selector[5]):
        #    state = state + 32

        #if GPIO.input(self.pins_selector[6]):
        #    state = state + 64

        #if GPIO.input(self.pins_selector[7]):
        #    state = state + 128

        setHMI[state]

        # Create demos here? Otherwise, state is returned as the final value
    def demo_1(self):
        pass


