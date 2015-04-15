##
# Drive.py: Class implementing differential drive abstraction layer over
#           Sabertooth module.
#
# Copyright 2015, Egan McComb
#
##

from Sabertooth.Sabertooth import Sabertooth as Sabertooth

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
                radius:    radius of turning with respect inner wheel (m)

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

        # Straight driving.
        if turn == "no":
            # Calculate speed percentage.
            speed = int(float(speed//speed_max*100))
            # Command motor driver.
            self.saber.mixedDrive(direction, speed)
