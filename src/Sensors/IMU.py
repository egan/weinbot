##
# IMU.py: Class implementing reading of IMU using RTIMULib.
#
# Copyright 2015, Egan McComb
#
##

from __future__ import division
import RTIMU
import threading
import time
import logging

class IMU():
    """
        IMU: A class to read yaw from the IMU using the quaternion SLERP Kalman
             filter algorithm provided by RTIMULib.
    """

    def __init__(self, settings="RTIMULib"):
        """
            settings: Basename of the RTIMULib settings file.

        """
        s = RTIMU.Settings(settings)
        self.imu = RTIMU.RTIMU(s)
        self.go = True

        if (not self.imu.IMUInit()):
            logging.debug("imu: initialization failed")
            self.go = False
            return None
        else:
            logging.debug("imu: initialization successful")

        # IMU Kalman fusion parameters.
        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.poll_interval = self.imu.IMUGetPollInterval()/1000

        # Start IMU read thread.
        t = threading.Thread(target=self.__handler)
        logging.debug("imu: reading started")
        t.start()

        return None

    def __del__(self):
        self.go = False

    def accelX():
        """
            accelX(): Return longitudinal acceleration (m/s^2).

        """
        return self.data["accel"][0]

    def accelY():
        """
            accelY(): Return lateral acceleration (m/s^2).

        """
        return self.data["accel"][1]

    def accelZ():
        """
            accelZ(): Return heave acceleration (m/s^2).

        """
        return self.data["accel"][2]

    def yaw():
        """
            accelZ(): Return yaw angle (deg).

        """
        return math.degrees(self.data["fusionPose"][2])

    def __handler(self):
        while True:
            if (self.go):
                # XXX: Always returns false.
                if self.imu.IMURead():
                    self.data = self.imu.getFusionData()
                    time.sleep(self.poll_interval)
                else:
                    logging.debug("imu: failed to read")
                    time.sleep(self.poll_interval)
            else:
                logging.debug("imu: reading halted")
                return
