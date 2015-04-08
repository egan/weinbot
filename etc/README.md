# Configuration Files
## Network Profiles (`netctl`)
The files `enp0s20u4-static` and `usb0-static` are example `netctl` profiles.
Please see the [documentation](../docs/connecting.md) for more information.

## Resolvconf Configuration
The file `resolvconf.conf` is an example `resolvconf` configuration to manually specify Google's DNS so that name resolution is available reliably.

## SSH Client Profile
The file `ssh_config` is an example SSH client config to be placed at `~/.ssh/config`.
With it, the user can do `ssh weinbot` rather than `ssh dev@192.168.10.42`.
