#!/bin/bash

##
# notes   -- outputs: LEDS after 330Ωresistor from pins 12, 14, 15, and 16 o
#             header P9.
#            inputs:  AIN0 0-5kΩ potentiometer hooked to 3.3 to 1.8voltage
#             divider from DC_3.3V supply.
#
# written -- 26 May 2013 by John Clark
#            http://www.armhf.com/using-beaglebone-black-gpios
#
# revised -- 1 April 2015 by Egan McComb
##

setup()
{
	# Enable digital GPIO pins 15, 13, 16, and 12.
	if [ ! -d /sys/class/gpio/gpio48 ]; then echo 48 > /sys/class/gpio/export; fi
	if [ ! -d /sys/class/gpio/gpio50 ]; then echo 50 > /sys/class/gpio/export; fi
	if [ ! -d /sys/class/gpio/gpio51 ]; then echo 51 > /sys/class/gpio/export; fi
	if [ ! -d /sys/class/gpio/gpio60 ]; then echo 60 > /sys/class/gpio/export; fi
	# Enable ANIN pins.
	if [ ! -e /sys/devices/ocp.3/helper.15/AIN0 ]; then echo cape-bone-iio /sys/devices/bone_capemgr.9/slots; fi
}

zero() {
	echo low > /sys/class/gpio/gpio48/direction
	echo low > /sys/class/gpio/gpio50/direction
	echo low > /sys/class/gpio/gpio51/direction
	echo low > /sys/class/gpio/gpio60/direction
}

##---MAIN----##
# Enable pins if necessary.
setup
# Clear.
zero
# Trap SIGINT to clear.
trap zero SIGINT SIGKILL
# Count.
for (( i=0 ; ; ++i ))
do
	# Read input voltage (0-1800mV).
	V=$(cat /sys/devices/ocp.3/helper.15/AIN0)

	# Calculate delay time (0.5-0.05s).
	t=$(echo '0.05+0.00025*' $V | bc)

	# Reset on overflow.
	if (( i > 0x0f )); then
		i=0
	fi

	# Calculate bit values from i.
	bit0=$(( (i & 0x01) > 0 ))
	bit1=$(( (i & 0x02) > 0 ))
	bit2=$(( (i & 0x04) > 0 ))
	bit3=$(( (i & 0x08) > 0 ))

	# Write output bits.
	echo $bit0 > /sys/class/gpio/gpio60/value
	echo $bit1 > /sys/class/gpio/gpio50/value
	echo $bit2 > /sys/class/gpio/gpio48/value
	echo $bit3 > /sys/class/gpio/gpio51/value

	# Sleep for delay time t.
	sleep $t
done
