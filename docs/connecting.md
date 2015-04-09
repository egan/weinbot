# Connecting to the BBB from Local Host
The following documentation was produced with an Arch Linux host in mind, but should be adaptable to other UNIX-like operating systems.

## Ethernet LAN
The Arch Linux ARM (ALARM) installation on the BBB will connect to an Ethernet LAN automatically if available.
To connect to the BBB from your local host, you must first determine its assigned IP address.
This can be accomplished in many ways, e.g. assuming you are on a 192.168.1.0/24 subnet, you may try:

	$ sudo nmap -sP 192.168.1.0/24

to obtain a list of hostnames with their MAC addresses.
Note that scans of this nature can be considered illegal in some jurisdictions so it is best that you do this on a LAN to which you have administrative rights, which should be the case anyway.
If you have administrative access to the gateway router for the LAN, router configuration portals often give the same information.

Once you have the IP address of the BBB, you may connect to it over SSH with e.g.:

	$ ssh dev@192.168.7.2

with the appropriate IP address substituted.
You may then configure host aliases and configuration for your SSH client as desired.

## USB LAN
The BBB has the capability to do TCP/IP over the mini-USB connector so that no separate Ethernet is required.

### Preconfiguration
The required preconfiguration has already been performed on the current BBB ALARM image, but is included below for completeness.
#### Kernel Module
In order to use the USB networking, the USB gadget Ethernet device module `g_ether` needs to be loaded with `modprobe`.
To load this module automatically on boot:

	# echo g_ether > /etc/modules-load.d/g_ether.conf

You can check that the module has been successfully loaded with `lsmod`.
A new network device (likely `usb0`) will be listed by `ip link show`.
#### Netctl Profile
In order to associate an IP on the `usb0` network device, a netctl profile is required.
An example profile is given [here](../etc/usb0-static).

The BBB client was given a static IP address 192.168.10.42; it is hoped that its situation outside the 192.168.1.0/8 subnet will reduce the risks of address collision.
It is assumed that the local host can associate with the address 192.168.10.3 on the 192.168.10.0/8 subnet so this is set as the gateway address to allow Internet access on the BBB.
Should these address selections conflict with your existing LAN change them as necessary.

The USB network can be brought up with `sudo netctl start usb0-static`.
To enable the profile permanently and have it started automatically on boot, do `sudo netctl enable usb0-static`.
#### DNS Resolution
In order to have working DNS, an appropriate name server should be configured in `/etc/resolv.conf`.
On the current BBB ALARM image, we use Google's DNS 8.8.8.8.

### Configuration
Once the BBB client network profile is functional the local host must be configured to connect with the USB LAN.
#### Netctl Profile
Check the name of the USB LAN device with `ip link show`.
In our example, it is `enp0s20u4`.

The local host needs an IP address on the USB LAN 192.168.10.0/8 subnet so that it may communicate with the BBB.
This address should be the same as the default gateway defined in the BBB network profile.
An example profile is given [here](../etc/enp0s20u4-static).

Upon bringing this profile up, you may connect to the BBB over SSH with:

	$ ssh dev@192.168.10.42

which is adequate for most administrative tasks.
#### Internet Access
Should Internet access on the BBB be required, network address translation and packet forwarding on the local host needs to be configured.
This can be accomplished running the `iptablescfg` script given [here](../bin/iptablescfg) as root.
The BBB should now have Internet access via the local host's connection.

## Troubleshooting
If `netctl` profiles fail to come up, check `journalctl -xe` and `systemctl status netctl@profile_name` as root for error messages.
One problem encountered was `RTNETLINK answers: File exists` due to a faulty `resolvconf` configuration.
In such a situation, the interface affected can be fixed with e.g.:

	# ip addr flush dev usb0
