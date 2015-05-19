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

        def dummy():
            pass

        self.drive = drive
        self.startFunc = dummy
        self.stopFunc = dummy
        self.go = True
        self.lock = False

        return None

    def __del__(self):
        self.stop()

    def path(self, path_spec, startFunc, stopFunc, delay=10):
        """
            path: Implement thread to iterate through list of path commands.

                startFunc: Function to call on path start.
                stopFunc:  Function to call on path end.
                path_spec: List of (direction, speed, turn, radius, time) tuples to specify the drive path.
                delay:     Initial delay time (s) before starting path.

        """
        if self.lock:
            logging.warning("path: busy")
        else:
            self.path_spec = path_spec
            self.startFunc = startFunc
            self.stopFunc = stopFunc
            self.delay = delay
            self.lock = True
            t = threading.Thread(target=self.__handler)
            t.start()

    def stop(self):
        """
            stop: Cancel the path and stop drive.

        """
        logging.debug("path: stopped")
        self.go=False
        # This call to drive.stop() is not extraneous, do not remove.
        self.drive.stop()
        self.stopFunc()

    def __handler(self):
        time.sleep(self.delay)
        logging.debug("path: starting path")
        self.startFunc()
        # Iterate through list of path commands.
        for cmd in self.path_spec:
            if self.go:
                logging.debug("path: maintain for %ds" %(cmd[4]))
                ret = self.drive.drive(cmd[0], cmd[1], cmd[2], cmd[3])
                # Cancel if command malformed.
                if ret == -1:
                    logging.debug("path: illegal drive command, path cancelled")
                    return

                # Sleep until next command.
                time.sleep(cmd[4])

        self.drive.stop()
        self.stopFunc()
        self.lock = False
        logging.debug("path: finishing path")
