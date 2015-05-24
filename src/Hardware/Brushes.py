##
# Brushes.py: Class implementing control of WEINBot brush motor relay via
#             GPIO.
#
# Copyright 2015, Egan McComb
#
##

from __future__ import division
import Adafruit_BBIO.GPIO as GPIO
import logging
import serial
import threading
import time

class Brushes():
    """
        Brushes: A class that provides an interface to control the WEINBot
                 brush motor relay via GPIO and simple serial.
    """

    def __init__(self, pin="P8_11", port="ttyO1", rampTime=2):
        """
            pin:      BBB GPIO pin to control brush motor relay.
            port:     Teletypewriter device to connect to.
            rampTime: Time in to ramp (s).

        """

        # Set up GPIO.
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

        # Set up serial.
        self.port = port
        self.saber = serial.Serial()
        self.saber.baudrate = 9600
        self.saber.port = '/dev/%s' % (self.port)
        self.saber.open()
        self.isOpen = self.saber.isOpen()

        # Parameters
        self.rampTime = rampTime
        self.steps = 4
        return None

    def __del__(self):
        self.stop()
        return

    def start(self):
        """
            start: Start the brush motors.

        """
        logging.debug("brushes: started")
        GPIO.output(self.pin, GPIO.HIGH)
        t = thread.Thread(target=self.__ramp)
        t.start()
        return

    def __ramp(self):
        tstep = self.rampTime/3
        logging.debug("brushes: 25%")
        self.saber.write(95)
        time.sleep(tstep)
        logging.debug("brushes: 50%")
        self.saber.write(63)
        time.sleep(tstep)
        logging.debug("brushes: 75%")
        self.saber.write(31)
        time.sleep(tstep)
        logging.debug("brushes: 100%")
        self.saber.write(0)
        return

    def stop(self):
        """
            stop: Stop the brush motors.

        """
        logging.debug("brushes: stopped")
        self.saber.write(127)
        GPIO.output(self.pin, GPIO.LOW)
