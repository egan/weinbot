# LIDAR-Lite Interface
To make a measurement, write register `0x00` with a value of `0x04`, which performs DC stabilization cycle, signal acquisition, and data processing.
Either wait 20ms or poll for an `ACK` before reading.
Register `0x0F` contains the upper 8bits of the measured distance in centimeters, and `0x10` the lower 8 bits.
Reading 1word from register `0x8F` will return the full distance--- *note that the byte order is reversed*.

For a full listing of the available control registers, refer to the [documentation](http://kb.pulsedlight3d.com/support/solutions/articles/5000549537-control-registers).
