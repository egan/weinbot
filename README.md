# WEINBot
The Water-Efficient Industrial Navigating Robot (WEINBot) is a proof-of-concept automated industrial floor care vehicle that can effectively dislodge and collect solid grape waste from typical concrete winery flooring with minimal water use.
Successful collection of solid waste before manual hose-down greatly reduces the labor and water requirements during crush season, when typical cleanings are a tedious chore that can use hundreds of gallons of water.
While the device does not have the full array of sensors and software algorithms to robustly navigate the uncontrolled winery environment, basic control and sensor technologies are included so that limited demonstrations of those functionalities required for full autonomy may be accomplished.
In this way, our device will serve as a good foundation for potential further robotics research to develop the automation techniques required to navigate the bustling winery environment.

# Documentation
## Administration and Development
### [Initial Operating System Configuration](docs/os_config.md)
### [Connecting to the BBB from Local Host](docs/connecting.md)
### [User Environment Configuration](docs/user_config.md)
### [Hardware Configuration](docs/hardware_config.md)

## Hardware
### [BeagleBone Black Reference Manual](docs/BBB_SRM.pdf)
### [BeagleBone Black Pin Maps](docs/pinmaps.md)
### [Sabertooth Motor Driver Reference](docs/Sabertooth2x60.pdf)
### [WEINBot Pin Assignments](docs/pinout.md)
### [IMU Communication and Calibration](docs/imu.md)
### [LIDAR-Lite Interface](docs/lidar.md)

## Operation and Demonstration
### [Deploying the WEINBot Software](docs/deploy.md)
### [Path Module Interface](docs/path.md)
### [HMI Functions](docs/demos.md)

## Software Architecture
The [`launch.c`](src/launch.c) program, which compiles to `weinbot` by the software [`deploy`](bin/deploy) script is a `setuid` binary which loads the privileged Python 2 interpreter required for the [main WEINBot operating system](src/weinbot.py) to run.

The WEINBot OS can be run in interactive mode in `ipython2` for debugging purposes.
It is very mildly engineered and is meant to be used as test code for the control modules.
When run in headless mode from the launcher, it runs in an infinite input loop, reading commands from the [`HMI`](src/Hardware/HMI.py) module, which returns a balanced ternary tuple representing the state of the four single pole, double throw toggle switches.
The `HMI` tuples are the keys in the `dispatcher` dictionary whose values are lambda functions to be called when the trigger is received.
The mode operation supervisor can also check the state of the load cell to signal when the waste bucket requires emptying.

### Drive Modules
#### [`Drive`](src/Drive/Drive.py)
This module is an abstraction layer over the `Sabertooth` module.
It provides a useful `drive()` method that enforces speed limits and is parameterized to reflect the dimensions of the vehicle.
These parameters are set in the initializer; artificial speed limits are required for both safety and the allowance of turns at maximum speed.
Drive commands are given in terms of tangential speed and turning radius, so that any path can be created.
Inside a critical radius, tangential speed is measured in angular units for more intuitive control that allows in-place turning.

### [`Sabertooth`](src/Drive/Sabertooth/Sabertooth.py)
This is an atomic module implementing control of the Sabertooth motor driver over packetized serial.
It provides a dictionary of plaintext commands for both independent and mixed mode driving corresponding to their hexadecimal message specifications.

### Hardware Modules
#### [`Alarm`](src/Hardware/Alarm.py)
This is an atomic module implementing on/off control of the alarm relay, tone selection, and timed strobing.
Tone selection via the `setTone()` method can be accomplished by numeric or string identifier; string identifiers can be used to associate tone numbers with implementation semantics.
Strobing via the `strobe()` method spawns a threaded handler taking a list of toggle times for the alarm.

#### [`Brushes`](src/Hardware/Brushes.py)
This is an atomic module consisting simply of on/off control of the brush motor relay.

#### [`Conveyor`](src/Hardware/Conveyor.py)
This is an atomic module consisting simply of on/off control of the conveyor motor relay.

#### [`HMI`](src/Hardware/HMI.py)
This is an atomic module consisting of a `__switchState()` utility method that detects the state of a given switch and any electrical faults in it.
The state of the whole array is returned by the `read()` method only if the trigger switch is activated, and only if it had been reset prior.

#### [`Pump`](src/Hardware/Pump.py)
This is an atomic module consisting simply of on/off control of the pump relay.

#### [`ServoSweep`](src/Hardware/ServoSweep.py)
This is a test module implementing on/off control of continuous sweeping of a servomotor via varying PWM duty cycle in a threaded timer handler `__servoSweep()`.
Sweeping is accomplished by setting specific maximum and minimum duty cycles at regular intervals.
At this time there is no interface with the `Lidar` module, and a future one may require more sophisticated control of the servomotor position to ensure synchronicity.

#### [`Shutoff`](src/Hardware/Shutoff.py)
This is an atomic module that registers a edge trigger interrupt on the emergency stop button detection circuit.
Its initializer takes a list of control objects for which to call their `stop()` methods on when the trigger event is received.
The interrupt callback is the `shutdown()` method, which can also be called freely to ensure all attributed hardware objects are stopped.

### Navigate Modules
The navigate modules are meant to include various algorithms for path planning and reactive navigation.
Currently there is only one module available, the open-loop dumb controller `Path`

#### [`Path`](src/Navigate/Path/Path.py)
This is an atomic module taking an instance of a `Drive` object and implementing timer-based control of it in a threaded handler with the ability to call utility functions at the start and end of the path specification.
More information is available [here](docs/path.md).

### Sensor Modules
#### [`IMU`](src/Sensors/IMU.py)
This is an atomic module that manages the interface with the IMU and calculates useful data therefrom.
It relies on the RTIMULib module.
When the module is initialized, it spawns a threaded handler `__imuSample()` that continuously reads pose data from the IMU at the ideal sampling rate.
However, access to this data can be asynchronous, with the various read methods for acceleration and attitude returning appropriately converted values utilizing the latest Kalman-filtered pose.
The threaded handler runs continuously until the object's `go` attribute is set to `False`.

#### [`Lidar`](src/Sensors/Lidar.py)
This is an atomic module that provides an interface to read the distance from the LIDAR-Lite rangefinder.
It relies on the `python-smbus` module for I²C communication, which is the primary dependency requiring the use of Python 2 over Python 3.
It simplistically waits out the sample time rather than polling for an `ACK`, which a more rigorous implementation would do.

#### [`LoadCell`](src/Sensors/LoadCell.py)
This is an atomic module that provides an interface to read the load cell in a dimensionless fashion.
