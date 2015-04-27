##
# Hardware.py: Class implementing control of WEINBot Load Cell.
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

    def read_load(self):
        """
            start: Read the load cell value.

        """
        logging.debug("reading load cell value")
        weight_reading = ADC.read(self.pin) 

    def sleep_load(self):
        """
            stop: Stop reading values from the load cell.

        """
        logging.debug("stopped reading load cell values")
        GPIO.output(self.pin, GPIO.IN)