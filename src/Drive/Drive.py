##
# Drive.py: Class implementing differential drive abstraction layer over
#           Sabertooth module.
#
# Copyright 2015, Egan McComb
#
##

from __future__ import division
from Sabertooth.Sabertooth import Sabertooth as Sabertooth
import logging
import math

class Drive():
    """
        Drive: A class that abstracts Sabertooth to useful differential drive
               commands. This class is not meant to be sufficient for
               controlled operation of a vehicle. An additional abstraction
               layer to take vehicle dynamics into account is recommended.
    """

    def __init__(self, speed_max=1.654, speed_limit=(1, 90), track=0.656, rcrit=1, ramp=15):
        """
            speed_max:   Maximum physical speed of drive motors (m/s).
            speed_limit: Tuple: speed limit for forward/reverse drive
                         operations (m/s), speed limit for tight turns (deg/s).
            track:       Track width for the drive wheels (m).
            rcrit:       Critical radius inside which speeds measured angularly.
            ramp:        Sabertooth ramp identifier.

        """

        # Drive system parameters.
        self.speed_max = speed_max
        self.speed_limit = speed_limit
        self.track = track
        self.rcrit = rcrit
        self.ramp = ramp

        if (self.speed_limit[0] > self.speed_max):
            return None

        # Instantiate motor driver object (com. over UART4).
        TTY = "ttyO4"
        self.saber = Sabertooth(TTY)
        if (self.saber == None):
            return None
        self.saber.setRamp(self.ramp)
        return None

    def __del__(self):
        self.saber.stop()
        return

    def drive(self, direction="fwd", speed=0, turn="no", radius=0.25):
        """
            drive: Drive in specified direction at specified speed with
                   specified radius of turning. Note that it is recommended
                   that the control layer bring the vehicle to a stop before
                   allowing the radius of turning to cross the critical value.

                direction: fwd or rev. Corresponds to CCW or CW for a left
                           turn, CW or CCW for right turn
                speed:     tangential speed (m/s)
                turn:      left, no, or right
                radius:    radius of turning with respect to axle center

        """
        # Stupidity checks.
        validcmds = ["fwd", "rev"]
        if (direction not in validcmds):
            return -1

        validcmds = ["left", "no", "right"]
        if (turn not in validcmds):
            return -1

        if radius < 0:
            radius = 0

        # Drive algorithm.
        if turn == "no":
            # Check speed limit. Ignore if malformed.
            if speed < 0:
                return -1
            elif speed > self.speed_limit[0]:
                return -1
            # Calculate speed percentage.
            speed = int(speed/self.speed_max*100)
            # Debug logging.
            logging.debug("drive (straight): %s %d" %(direction, speed))
            # Command motor driver.
            self.saber.independentDrive(direction, speed, direction, speed)
        else:
            if radius >= self.rcrit:
                # Check speed limit.
                if speed < 0:
                    return -1
                elif speed > self.speed_limit[0]:
                    return -1
                # Wheel speeds assuming left turn.
                speed_l = speed*(2*radius - self.track)/(2*radius)
                speed_r = speed*(2*radius + self.track)/(2*radius)
                # Check for saturation.
                if speed_r > self.speed_max:
                    # Truncate speed to max attainable at turning radius.
                    logging.debug("drive (turn): speed truncated due to saturation")
                    speed_l = self.speed_max/speed_r*speed_l
                    speed_r = self.speed_max
                # Swap if turning right.
                if turn == "right":
                    speed_l, speed_r = speed_r, speed_l
                # Calculate speed percentages.
                speed_l = abs(int(speed_l/self.speed_max*100))
                speed_r = abs(int(speed_r/self.speed_max*100))
                # Debug logging.
                logging.debug("drive (turn): %s %d %s %d" %(direction, speed_l, direction, speed_r))
                # Command motor driver.
                self.saber.independentDrive(direction, speed_l, direction, speed_r)
            else:
                # Check speed limit.
                if speed < 0:
                    return -1
                elif speed > self.speed_limit[1]:
                    return -1
                # Convert speed to rad/s.
                speed = math.pi*speed/180
                # Wheel speeds assuming left turn.
                speed_l = speed*(2*radius - self.track)/2
                speed_r = speed*(2*radius + self.track)/2
                # Check for saturation.
                if speed_r > self.speed_max:
                    # Truncate speed to max attainable at turning radius.
                    logging.debug("drive (turn): speed truncated due to saturation")
                    speed_l = self.speed_max/speed_r*speed_l
                    speed_r = self.speed_max
                # Swap if turning right.
                if turn == "right":
                    speed_l, speed_r = speed_r, speed_l
                # Determine directions assuming driving forward.
                if speed_l < 0:
                    dir_l = "rev"
                else:
                    dir_l = "fwd"

                if speed_r < 0:
                    dir_r = "rev"
                else:
                    dir_r = "fwd"
                # Swap if driving reverse.
                if direction == "rev":
                    dir_l, dir_r = dir_r, dir_l
                # Calculate speed percentages.
                speed_l = abs(int(speed_l/self.speed_max*100))
                speed_r = abs(int(speed_r/self.speed_max*100))
                # Debug logging.
                logging.debug("drive (turn): %s %d %s %d" %(dir_l, speed_l, dir_r, speed_r))
                # Command motor driver.
                self.saber.independentDrive(dir_l, speed_l, dir_r, speed_r)


    def stop(self):
        """
            stop: Stops all drive using drive.

        """
        self.drive("fwd", 0)
