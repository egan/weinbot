##
# Sabertooth.py: Class implementing packetized serial control of
#                Sabertooth 2x60 motor driver (Dimension Engineering).
#
# Copyright 2015, Egan McComb
#
# This code was adapted from MIT licensed:
#
# > Sabertooth.py
# > Copyright 2014, Troy Dack
# > <https://github.com/tdack/BBB-Bot>.
#
##

import serial, logging
import Adafruit_BBIO.UART as UART

class Sabertooth():
    """
        Sabertooth: A class to control a Sabertooth 2x60 using the packetized
                    serial mode (DIP switches 1,2 low).

        https://www.dimensionengineering.com/datasheets/Sabertooth2x60.pdf
    """
    # Commands to implement. See pages 20-23 of the documentation for
    # additional commands available.
    cmds = {
            "fwd_left": 0x00,
            "rev_left": 0x01,
            "fwd_right": 0x04,
            "rev_right": 0x05,
            "fwd_mixed": 0x08,
            "rev_mixed": 0x09,
            "right_mixed": 0x0A,
            "left_mixed": 0x0B,
            "ramp": 0x10
            }

    def __init__(self, BBB_UART="UART1", port="/dev/ttyO1", address=128):
        """
            Beagle_UART: BBB UART to use (must be enabled in uEnv.txt).
            port:        Teletypewriter device to connect to.
            address:     Address of controller to send commands to
                         (set by DIP switches 3-6).

        """
        self.UART = BBB_UART
        self.port = port
        self.address = address

        if (self.UART == None) or (self.port == None) or (self.address < 128 or self.address > 135):
            return None

        # Setup UART on BeagleBone (loads device tree overlay).
        UART.setup(self.UART)

        # Initialize serial port.
        self.saber = serial.Serial()
        self.saber.baudrate = 9600
        self.saber.port = '/dev/%s' % (self.port)
        self.saber.open()
        self.isOpen = self.saber.isOpen()
        return None

    def __del__(self):
        self.stop()
        return

    def sendCommand(self, command, message):
        """
            sendCommand: Sends a packetized serial command to the Sabertooth
                         controller, returning bytes written.

                command: Command to send. Valid commands (as strings) are:
                    fwd_left
                    rev_left
                    fwd_right
                    rev_right
                    fwd_mixed
                    rev_mixed
                    right_mixed
                    left_mixed
                    ramp
                message: Command content, usually speed 0-100%.

        """
        # Calculate checksum termination (page 23 of the documentation).
        checksum = (self.address + command + message) & 127
        # Write data packet.
        sentBytes = self.saber.write("".join(chr(i) for i in [self.address, command, message, checksum]))
        # Flush UART.
        self.saber.flush()
        return sentBytes

    def independentDrive(self, dir_left="fwd", speed_left=0, dir_right="fwd", speed_right=0):
        """
            independentDrive: Independent drive (simultaneous command). Calls
                              sendCommand, returning bytes written.

                dir_left:    fwd or rev (left motor)
                speed_left:  0-100% speed (left motor)
                dir_right:   fwd or rev (right motor)
                speed_right: 0-100% speed (right motor)

        """
        # Stupidity checks.
        validcmds = ["fwd", "rev"]
        if (dir_left not in validcmds) or (dir_right not in validcmds):
            return -1

        if  speed_left < 0:
            speed_left = 0
        elif speed_left > 100:
            speed_left = 100

        if  speed_right < 0:
            speed_right = 0
        elif speed_right > 100:
            speed_right = 100

        # Calculate speed commands from percentages.
        speed_left = int((float(speed_left)*127)//100)
        speed_right = int((float(speed_right)*127)//100)

        # Debug logging.
        logging.debug("independentDrive: %s %d %s %d" %(dir_left + "_left", speed_left, dir_right + "_right", speed_right))

        # Send drive commands.
        sentBytes = self.sendCommand(self.cmds[dir_left + "_left"], speed_left)
        sentBytes += self.sendCommand(self.cmds[dir_right + "_right"], speed_right)

    def mixedDrive(self, direction="fwd", speed=0):
        """
            mixedDrive: Mixed drive (in-place turning and linear control).
                        Calls sendCommand, returning bytes written.

                direction: fwd, rev, left, or right.
        """
        # Stupidity checks.
        validcmds = ["fwd", "rev", "left", "right"]
        if  (direction not in validcmds):
            return -1

        if  speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        # Calculate speed command from percentage.
        speed = int((float(speed)*127)//100)

        logging.debug("mixedDrive: %s %d" %(direction + "_mixed", speed))

        sentBytes = self.sendCommand(self.cmds[direction + "_mixed"], speed)

    def stop(self):
        """
            stop: Stops both motors using mixedDrive, returning bytes written.

        """
        sentBytes = 0
        sentBytes = self.mixedDrive("fwd", 0)
        return sentBytes

    def setRamp(self, value):
        """
            setRamp: Set acceleration ramp for controller.

                value: Ramp value to use (see documentation):
                    01-10: Fast Ramp
                    11-20: Slow Ramp
                    21-80: Intermediate Ramp

        """
        sentBytes = 0
        if (value > 0 and value < 81):
            sentBytes = self.sendCommand(self.cmds["ramp"], value)
        else:
            return -1

        return sentBytes

