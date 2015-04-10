import Adafruit_BBIO.GPIO as GPIO
import fcntl
import os
import sys
import time

## Setup:
# Darlington Array:
#  1. Connect pin 8 (GND) to circuit common node.
#  2. Connect pins 1-3 (or any B pins) to BBB P9_{42, 44, 46}.
#  3. Connect pins 16-14 (or any corresponding C pins) to relay coil - pin.
#  4. Connect pin 9 (COM) to 5V signal branch.
#
# Power:
#  1. Set PSU to intermediate amperage, 5.0V.
#  2. Connect negative lead to circuit common node.
#  3. Connect positive lead to 5V power branch.
#  4. Connect power branch to signal branch.
#
# Relays:
#  1. Connect NO to load side.
#  2. Connect COM to power branch.
#  3. Connect coil + to signal branch.
#
# Loads:
#  1. Connect relay NO pin to LED via appropriate resistor (e.g. 1kÎ).
##

# Setup GPIO pins.
GPIO.setup("P8_42", GPIO.OUT)
GPIO.setup("P8_44", GPIO.OUT)
GPIO.setup("P8_46", GPIO.OUT)

# Basic 3 bit counter.
def count():
    for i in range(8):
        if ((i & 0x1) == 0x1):
            GPIO.output("P8_42", GPIO.HIGH)
        else:
            GPIO.output("P8_42", GPIO.LOW)

        if ((i & 0x2) == 0x2):
            GPIO.output("P8_44", GPIO.HIGH)
        else:
            GPIO.output("P8_44", GPIO.LOW)

        if ((i & 0x4) == 0x4):
            GPIO.output("P8_46", GPIO.HIGH)
        else:
            GPIO.output("P8_46", GPIO.LOW)

        # Delay time.
        time.sleep(0.05)

# Operating system voodoo.
fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)

# Run until return is received.
print("Type return to break on next overflow.")
while True:
    try:
        stdin = sys.stdin.read()
        if "\n" in stdin or "\r" in stdin:
            GPIO.cleanup()
            break
    except IOError:
        pass
        count()
