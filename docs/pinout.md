# WEINBot Pin Assignments

## UART
The motor driver is controlled over `UART4`, consuming pins `P9_{11, 13}`.

## I²C
Both exposed I²C buses are used, consuming pins `P9_{17..22, 24, 26}`.
The communication with the IMU is performed over `I2C1` and communication with the LIDAR-Lite (planned) is performed over `I2C2`.

## Analog Input
The load cell and conductivity sensor (planned) each require a single `AIN` pin:

-`P9_`: load cell
-`P9_`: conductivity sensor

## GPIO
### Digital Input

-: stop switch detection (1)
-: sensing edge switch detection (2?)
-: HMI SPDT switch detection (4, 8?)


### Digital Output

-: continuous duty motor control relays (3)
-: alarm siren and strobe select (10?)

## PWM
The LIDAR servomechanism (planned) is controlled with PWM, consuming pin `P8_`.
