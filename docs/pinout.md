# WEINBot Pin Assignments

## UART
The motor driver is controlled over `UART4`, consuming pins `P9_{11, 13}`.
At this time, only `P9_13` (`TX`) is used.

## I²C
Both exposed I²C buses are used, consuming pins `P9_{17..22, 24, 26}`.
The communication with the IMU is performed over `I2C1` and communication with the LIDAR-Lite (planned) is performed over `I2C2`.

## PWM
The LIDAR servomechanism (planned) is controlled with PWM, consuming pin `P8_46`.

## Analog Input
The load cell and tank sensor (planned) each require a single `AIN` pin:

* `P9_36`: load cell.
* `P9_38`: tank sensor.

## GPIO
### Digital Input

* `P9_41`: shutoff switch detection.
* `P8_{3, 4}`: sensing edge switch detection.
* `P8_{37..44}`: HMI SPDT switch detection.


### Digital Output

* `P9_42`: motor driver deadman's switch.
* `P8_{11..13}`: continuous duty motor control relays.
* `P8_{21..25}`: alarm siren select
* `P8_26`: alarm siren switch
