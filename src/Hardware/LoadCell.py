##
# Hardware.py: Class implementing control of WEINBot Human Machine Interface.
#
# Copyright 2015, Natalie Pueyo Svoboda
#
##

import Adafruit_BBIO.ADC as ADC
import logging

class LoadCell():
    """
        LoadCell: A class that provides an interface to read the WEINBot 
           load cell through AIN.
    """
        
    def __init__(self, pin="P9_36"):
        """
            pin: BBB AIN pin to control load cell.

        """

        # Set up ADC.
        self.pin = pin
        ADC.setup()
        return None

    def __del__(self):
        self.stop()
        return

    def start(self):
        """
            start: Read the load cell value.

        """
        logging.debug("reading load cell value")
        weight_reading = ADC.read(pin) # if that doesn't work, pin number replaces pin