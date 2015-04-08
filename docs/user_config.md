# User Environment Configuration
Some modifications from the default user enviroment configuration may be required.

## Terminal Information/Capabilities
Because the WEINBot ALARM installation is minimal, it may not have the proper terminfo/termcap for your local host terminal.
The default `rxvt` is set in `~/.bash_profile`; change this as necessary to suit your system.
Ad-hoc setting of $TERM can be accomplished by setting/exporting it on the BBB, or by prepending it to the ssh command line on the local host.
