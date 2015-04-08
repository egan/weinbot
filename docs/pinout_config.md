# Pinout Configuration
Because many of the exposed pins on the BBB are muxed, some configuration is required to enable and configure the appropriate I/O.

## UARTs
By default only UART0 (exposed on J1) is exposed.
To enable the others, edit the `uEnv.txt` file on the boot partition by appending e.g.:

	capemgr.enable_partno=BB-UART1

to the current configuration line.
Upon rebooting, the UART device should show in `/dev/ttyO*` (note that that is in fact the letter O, not zero).
