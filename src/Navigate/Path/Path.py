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

    def __init__(self, drive):
        """
            drive:     Drive object to command.

        """

        self.drive = drive
        self.lock = False

        return None

    def __del__(self):
        self.drive.stop()

    def path(self, path_spec, delay):
        """
            path: Implement thread to iterate through list of path commands.

                path_spec: List of (direction, speed, turn, radius, time) tuples to specify the drive path.
                delay:     Initial delay time (s) before starting path.

        """
        if self.lock:
            logging.debug("path: busy")
        else:
            self.path_spec = path_spec
            self.delay = delay
            self.lock = True
            t = threading.Thread(target=self.handler)
            t.start()

    def handler(self):
        time.sleep(self.delay)
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
        self.lock = False
        logging.debug("path: finishing path")
