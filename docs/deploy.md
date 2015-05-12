# Deploying the WEINBot Software
Deploy the WEINBot software by running the script `bin/deploy` given [here](../bin/deploy) as root.
This script will compile the [`setuid` launcher](../src/launcher.c) add the `setuid` permission bit, and copy the control software to `~wtf` for operation.
