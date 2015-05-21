# Hardware Configuration
Because many of the exposed pins on the BBB are muxed, some configuration is required to enable and configure the appropriate I/O.
To read general documentation on the SysFS interface to Linux GPIO, refer [here](gpio-sysfs.txt).

## Cape Manager
The device tree overlays (DTOs) are configured by the cape manager `capemgr`.
The enabled pinouts can be listed using:

	$ cat /sys/devices/bone_capemgr.*/slots

Those entries with `L` status are loaded.

To change what is loaded, edit the `uEnv.txt` file on the boot partition by appending `capemgr.enable_partno` and/or `capemgr.disable_partno` keys with comma delimited pinout identifiers and reboot.
The configuration used for WEINBot is given [here](../etc/uEnv.txt).

### Freeing up I/O from HDMI and eMMC
By default, many pins are unavailable for general use because they are tied to HDMI and eMMC buses.
To disable these, add the identifiers `BB-BONELT-HDMI`, `BB-BONELT-HDMIN`, and `BB-BONE-EMMC-2G` to the cape manager disable argument.

### UARTs
By default only UART0 (exposed on J1) is configured.
To enable the others, add the `BB-UART*` identifier to the cape manager enable argument.
Upon rebooting, the UART device should show up at `/dev/ttyO*` (note that that is in fact the letter O, not zero).
The UART3 (TX only) is special in that it cannot be loaded in this way; see [this resource](http://www.armhf.com/beaglebone-black-serial-uart-device-tree-overlays-for-ubuntu-and-debian-wheezy-tty01-tty02-tty04-tty05-dtbo-files/) for advanced information on how to configure all the UARTs.

### I2C Devices
By default only I2C0 (not pinned out) is configured.
To enable the others, add the `BB-I2C*` identifier to the cape manager enable argument.
Upon rebooting, the I2C buses should show up in the output of `i2cdetect -l`.
To poll I²C devices on a bus, do `i2cdetect -r -y $BUS` as root, where $BUS is the bus number.
A memory map will print showing the available chip addresses.

To write to an I²C device,

	# i2cset -y $BUS $CHIP_ADDRESS $DATA_ADDRESS $VALUE

To read from it,

	# i2cget -y $BUS $CHIP_ADDRESS $DATA_ADDRESS $TYPE

where `$TYPE` is `b` for byte or `w` for word.
