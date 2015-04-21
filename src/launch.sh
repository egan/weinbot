#!/bin/bash

##
# launch.sh: Launch WEINBot control software and watch for crashes.
#
# Copyright 2015, Egan McComb
##

logfile=weinbot.log

echo "Launching WEINBot control software" $(date) | tee >> $LOGFILE
{ python weinbot.py | tee >> $LOGFILE } || { echo "Unexpected exit: halting!" | tee >> $LOGFILE; echo 0 > /sys/class/gpio/gpio*/value }

exit 0
