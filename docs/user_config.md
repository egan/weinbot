# User Environment Configuration
Some modifications from the default user enviroment configuration may be required.

## Terminal Information/Capabilities
Because the WEINBot ALARM installation is minimal, it may not have the proper terminfo/termcap for your local host terminal.
Ad-hoc setting of `$TERM` can be accomplished by setting/exporting it on the BBB, or by prepending it to the ssh command line on the local host.
A better solution is to copy the terminfo profile from your local host at `/usr/share/terminfo/r` to the `~/.terminfo/r` directory on the BBB.
The `tmux` default terminal is set to `screen-256color` in `~/.tmux.conf`.
