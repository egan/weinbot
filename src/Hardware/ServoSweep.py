##
# ServoSweep.py: Class implementing control of WEINBot sweeping LIDAR
#                servomechanism.
#
# Copyright 2015, Egan McComb
#
##

from __future__ import division
import Adafruit_BBIO.PWM as PWM
import threading
import time
import logging

class ServoSweep():
    """
        ServoSweep: A class that implements back-and-forth sweeping of the
                    LIDAR servomechanism via BBB PWM.
    """

    def __init__(self, pin="P8_46", angle=120):
        """
            pin: BBB PWM pin to control servomotor.
            angle: Sweep angle (deg).

        """

        # Setup.
        self.pin = pin
        self.angle = angle
        self.lock = False
        # XXX: These parameters should be determined from angle.
        self.duty_min = 3
        self.duty_max = 12
        self.duty_span = self.duty_max - self.duty_min
        self.sweepInterval = 0.66
        # Start at minimum angle with 60Hz control signal.
        PWM.start(pin, 100-self.duty_min, 60)
        return None

    def __del__(self):
        self.stop()
        PWM.stop(self.pin)
        PWM.cleanup()
        return

    def start(self):
        """
            start: Start sweeping the servomotor.

        """
        # Don't spawn multiple thread handlers.
        if self.lock:
            return
        else:
            self.lock = True
            t = threading.Thread(target=self.__servoSweep)
            t.start()
            logging.debug("servo: starting sweep")

    def __servoSweep(self):
        while self.lock:
            PWM.set_duty_cycle(self.pin, self.duty_max)
            time.sleep(self.sweepInterval)
            PWM.set_duty_cycle(self.pin, self.duty_min)
            time.sleep(self.sweepInterval)

    def center(self):
        """
            center: Center the servomotor.

        """
        PWM.set_duty_cycle(self.pin, self.duty_min+(self.duty_max-self.duty_min)/2)
        return

    def stop(self):
        """
            stop: Stop sweeping the servomotor.

        """
        self.lock = False
        logging.debug("servo: stopping sweep")
        return
