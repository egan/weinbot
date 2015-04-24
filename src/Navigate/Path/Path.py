##
# Path.py: Class implementing path following by timed Drive commands.
#
# Copyright 2015, Egan McComb
#
##

import threading
import time
import logging

class Path():
    """
        Path: A class to implement open loop paths using timed thread. This
              class is not meant to be sufficient for controlled operation of
              the vehicle, so care in selecting path specifications should be
              exercised.
    """

    def __init__(self, drive, path_spec):
        """
            drive:     Drive object to command.
            path_spec: List of (direction, speed, turn, radius, time) tuples to
                       specify the drive path.

        """

        self.drive = drive
        self.path_spec = path_spec

        t = threading.Thread(target=self.handler)
        t.start()

        return None

    def __del__(self):
        self.drive.stop()

    def handler(self):
        logging.debug("path: starting path")
        # Iterate through list of path commands.
        for cmd in self.path_spec:
            logging.debug("path: maintain for %ds" %(cmd[4]))
            ret = self.drive.drive(cmd[0], cmd[1], cmd[2], cmd[3])
            # Cancel if command malformed.
            if ret == -1:
                logging.debug("path: illegal drive command, path cancelled")
                return

            # Sleep until next command.
            time.sleep(cmd[4])

        self.drive.stop()
        logging.debug("path: finishing path")
