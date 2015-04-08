from Sabertooth.Sabertooth import Sabertooth as Sabertooth

## Setup:
# Power:
#  1. Set the PSU to maximum amperage, 24.0V.
#  2. Connect negative lead to B- terminal.
#  3. Connect positive lead to B+ terminal.
#  4. Double check the power connections. Getting this wrong will
#     fry the motor driver!
#  5. Connect the motor leads the to M*{A,B} terminals.
# COM:
#  1. Connect any DGND to PSU ground.
#  2. Connect P9_24 to S1 terminal.
##

# UART1 must be enabled in uEnv.txt.
UART = "UART1"
TTY = "ttyO1"

# Instantiate motor driver object with correct hardware information.
saber = Sabertooth(UART, TTY)
# Set ramping.
saber.setRamp(15)

##
# Testing:
#  1. Turn on the power supply. The motor driver heat sink fan will
#     spool up and then stop. This is normal.
#  2. Run the preceding code in the interactive python console, e.g.
#     in ipython2.
#  3. Call the saber.driveMotor() method to set the speed and direction.
##
