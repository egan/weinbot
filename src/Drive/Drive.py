##
# Drive.py: Class implementing differential drive abstraction layer over
#           Sabertooth module.
#
# Copyright 2015, Egan McComb
#
##

from Sabertooth.Sabertooth import Sabertooth as Sabertooth
import logging

class Drive():
    """
        Drive: A class that abstracts Sabertooth to useful differential drive
               commands.
    """

    def __init__(self, speed_max=1.654, speed_limit=1, track=1, ramp=15):
        """
            speed_max:   Maximum physical speed of drive motors (m/s).
            speed_limit: Speed limit for forward/reverse drive operations (m/s).
            track:       Track width for the drive wheels.
            ramp:        Sabertooth ramp identifier.

        """

        # Drive system parameters.
        self.speed_max = speed_max
        self.speed_limit = speed_limit
        self.track = track
        self.ramp = ramp

        if (self.speed_limit > self.speed_max):
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
                   specified radius of turning.

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

        if speed < 0:
            speed = 0
        elif speed > self.speed_limit:
            speed = self.speed_limit

        if radius < 0:
            radius = 0

        # Drive algorithm.
        # XXX: Check for saturation in turns, add speed limit for turns with
        # internal radii.
        if turn == "no":
            # Calculate speed percentage.
            speed = int(float(speed/self.speed_max*100))
            # Debug logging.
            logging.debug("drive (straight): %s %d" %(direction, speed))
            # Command motor driver.
            self.saber.independentDrive(direction, speed, direction, speed)
        else:
            # Wheel speeds assuming left turn.
            if radius == 0:
                speed_l = -speed
                speed_r = speed
            else:
                speed_l = speed*(2*radius - self.track)/(2*radius)
                speed_r = speed*(2*radius + self.track)/(2*radius)
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
            speed_l = abs(int(float(speed_l/self.speed_max*100)))
            speed_r = abs(int(float(speed_r/self.speed_max*100)))
            # Debug logging.
            logging.debug("drive (turn): %s %d %s %d" %(dir_l, speed_l, dir_r, speed_r))
            # Command motor driver.
            self.saber.independentDrive(dir_l, speed_l, dir_r, speed_r)


    def stop(self):
        """
            stop: Stops all drive using drive.

        """
        self.drive("fwd", 0)
