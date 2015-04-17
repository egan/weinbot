##
# weinbot.py: Master program for WEINBot.
#
# Copyright 2015, Egan McComb
#
##

# External libraries and modules.
from __future__ import division
import logging

# In-house libraries and modules.
from Drive.Drive import Drive as Drive
from Hardware import *

# Logging.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initialization.
alarm = Alarm()
brushes = Brushes()
drive = Drive()
