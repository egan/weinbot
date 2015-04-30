# IMU Communication and Calibration
The WEINBot project uses the excellent [RTIMULib](https://github.com/richards-tech/RTIMULib) library to read and interpret data from the IMU.
It supports a range of sensors, and can produce Kalman-filtered quaternion SLERP pose data from sensor fusion.

## Testing the IMU
To test the IMU with Python, refer to the `tests` directory in the [python module](https://github.com/richards-tech/RTIMULib/tree/master/Linux/python).
If the IMU is connected appropriately over I²C, it should be automatically detected and configured.
This configuration is saved by the library in `RTIMULib.ini`, which may be edited for further customization.

## Calibrating the IMU
To calibrate the IMU with a text interface, compile and run [`RTIMULibCal`](https://github.com/richards-tech/RTIMULib/tree/master/Linux/RTIMULibCal) and follow the on screen instructions.
To perform an ellipsoid fit for the magnetometer, the `octave` package is required which brings in `libgl` dependencies.
The calibration data is output or saved in the configuration file `RTIMULib.ini`.
