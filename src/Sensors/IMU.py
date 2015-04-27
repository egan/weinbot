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
import math

class IMU():
    """
        IMU: A class to read yaw from the IMU using the quaternion SLERP Kalman
             filter algorithm provided by RTIMULib.
    """

    def __init__(self, settings="RTIMULib"):
        """
            settings: Basename of the RTIMULib settings file.

        """
        self.s = RTIMU.Settings(settings)
        self.imu = RTIMU.RTIMU(self.s)
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
        t = threading.Thread(target=self.__imuSample)
        t.start()
        logging.debug("imu: reading started at %dms sample period" %(self.poll_interval*1000))

        return None

    def __del__(self):
        self.go = False

    def accelX(self):
        """
            accelX(): Return longitudinal acceleration (m/s^2).

        """
        return self.data["accel"][0]*9.81

    def accelY(self):
        """
            accelY(): Return lateral acceleration (m/s^2).

        """
        return self.data["accel"][1]*9.81

    def accelZ(self):
        """
            accelZ(): Return heave acceleration (m/s^2).

        """
        return self.data["accel"][2]*9.81

    def yaw(self):
        """
            accelZ(): Return yaw angle (deg).

        """
        return math.degrees(self.data["fusionPose"][2])

    def __imuSample(self):
        while self.go:
            if self.imu.IMURead():
                self.data = self.imu.getIMUData()

            time.sleep(self.poll_interval)

        logging.debug("imu: reading halted")
        return
