##
# Lidar.py: Class implementing reading of LIDAR over I2C.
#
# Copyright 2015, Egan McComb
#
##

from __future__ import division
from Adafruit_I2C import Adafruit_I2C
import time
import logging

class Lidar():
    """
        Lidar: A class that provides an interface to read the PulsedLight LIDAR
               LITE rangefinder over I2C.
    """

    def __init__(self, address=0x62, bus=-1):
        """
            address: I2C data address for range information.
            bus:     I2C bus name (-#).

        """

        # Set up I2C.
        self.lidar = Adafruit_I2C(address, bus)
        return None

    def read(self):
        """
            read: Read the distance from the LIDAR.

        """
        # Perform DC stabilization cycle, signal acquisition and data
        # processing.
        s = self.lidar.write8(0x00, 0x4)
        if s == -1:
            return -1
        # Read 2 bytes data, reversed (cm).
        time.sleep(0.02)
        return self.lidar.reverseByteOrder(self.lidar.readU16(0x8F))

