# Initial Operating System Configuration
The BBB single board computer (SBC) runs Arch Linux ARM (ALARM) off the micro SD card.

## Installation
The OS and boot loader can be installed to the SD card from any computer following the [instructions](http://archlinuxarm.org/platforms/armv7/ti/beaglebone-black).
Note that the tape archive extraction of the boot loader may fail due to ownership issues on the FAT partition.
This can be worked around by adding the `--no-same-owner` flag to `tar`.

The root password was set, the hostname was changed to `weinbot` in `/etc/hostname` and `/etc/hosts`, and the appropriate timezone was configured with:

	# ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

Other than this, the basic configuration of the default image suffices.
For a list of installed software, refer to the [package list](pkg.txt).

## User Structure
Two users were added to the group `users`, `dev` and `wtf` (for Wash the Floor¡).
The `dev` user is the development and administration user, having `sudo` access as a member of the `wheel` group (enabled with `visudo`).
The `wtf` user is unprivileged and is the user in which the robot operating system and control software will be run.
Similar to `root`, it should not be accessed directly.

## User Configuration
User configuration files for the `dev` account are obtained from <https://github.com/egan/dotfiles>.
Some useful utilities are included from <https://github.com/egan/scripts>.
Refer to those resources for documentation.

## Booting Straight to SD
To facilitate unattended boot straight to SD (rather than internal eMMC), merely zero out the onboard boot partition with `dd`.
**Note that this will destroy data on the referenced volume!**

## Automatic Login of Operative User `wtf`
To automatically login user `wtf`, add the `systemd` `getty` service [override](../etc/override.conf) to `/etc/systemd/system/getty@tty1.service.d/override.conf`.
On reboot, the user `wtf` should be shown in the output of `w` as logged in on `tty1`.
Automatic running of software as this user can be accomplished by editing their `.bash_profile` configuration file.
It is recommended that programs be run inside the terminal multiplexer `tmux` so that one may attach to the appropriate session to monitor and control its operation.
