##
# LoadCell.py: Class implementing reading of WEINBot load cell.
#
# Copyright 2015, Natalie Pueyo Svoboda
#
##

import Adafruit_BBIO.ADC as ADC
import logging

class LoadCell():
    """
        LoadCell: A class that provides an interface to read the WEINBot load
                  cell through AIN.
    """

    def __init__(self, pin="P9_36"):
        """
            pin: BBB AIN pin to control load cell.

        """

        # Set up ADC.
        self.pin = pin
        ADC.setup()
        return None

    def read(self):
        """
            read: Read the load cell value (normalized).

        """
        logging.debug("loadcell: reading load cell value")
        weight_reading = ADC.read(self.pin)

