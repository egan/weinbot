# WEINBot Pin Assignments

## UART
The motor driver is controlled over `UART4`, consuming pins `P9_{11, 13}`.
Only `P9_13` (`TX`) is used.

The brush motor driver is controlled over `UART1`, consuming pins `P9_{24, 26}`.
Only `P9_24` is used.

## I²C
The communication with the IMU and LIDAR-Lite is performed over bus `I2C1`, consuming pins `P9_{17..22}`.

There is an error in the official pinmap with respect to the I²C pins on the rev.A BBB.
The working pins are as follows for bus 1:
* `P9_19`: IMU clock
* `P9_20`: IMU data

## PWM
The LIDAR servomechanism is controlled with PWM, consuming pin `P8_46`.

## Analog Input
The BBB's ADC consumes pins `P9_{32..40}`.
The load cell and flow sensor (planned) each require a single `AIN` pin:

* `P9_36`: load cell.
* `P9_38`: flow sensor.

## GPIO
### Digital Input

* `P9_42`: shutoff switch detection.
* `P8_{3, 4}`: sensing edge switch detection.
* `P8_{37..44}`: HMI SPDT switch detection.


### Digital Output

* `P8_{11..13}`: continuous duty motor control relays.
	* `P8_11`: brush motors relay
	* `P8_12`: conveyor motor relay
	* `P8_13`: pump relay
* `P8_{21..25}`: alarm siren select
* `P8_26`: alarm siren switch
