# WEINBot Pin Assignments

## UART
The motor driver is controlled over `UART4`, consuming pins `P9_{11, 13}`.

## I²C
Both exposed I²C buses are used, consuming pins `P9_{17..22, 24, 26}`.
The communication with the IMU is performed over `I2C1` and communication with the LIDAR-Lite (planned) is performed over `I2C2`.

## PWM
The LIDAR servomechanism (planned) is controlled with PWM, consuming pin `P8_{46}`.

## Analog Input
The load cell and conductivity sensor (planned) each require a single `AIN` pin:

* `P9_{36}`: load cell
* `P9_{38}`: conductivity sensor

## GPIO
### Digital Input

* `P9_{41}`: stop switch detection (1)
* `P8_{3,4}`: sensing edge switch detection (2?)
* `P8_{37...44}`: HMI SPDT switch detection (4, 8?)


### Digital Output

* `P8_{11...13}`: continuous duty motor control relays (3)
* `P8_{21...25}`: alarm siren and strobe select (10?)
