#!/bin/bash

##
# resetgpio.sh: Reset all GPIO on BBB.
#
# Copyright 2015, Egan McComb
#
##

echo "Unexpected exit: halting!"
echo 0 > /sys/class/gpio/gpio*/value

exit 0
