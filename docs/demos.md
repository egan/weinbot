# HMI Functions
The current human machine interface (HMI) is an array of four two-way toggle switches.
The middle position is neutral, the up position is + and the bottom position is $-$.
The WEINBot is commanded by arranging the triad of these switches in a specific configuration and activating it with the lone (trigger) switch.
Once activated, a new command cannot be entered until the command operation is completed (or canceled via emergency stop).
Additionally, **the trigger switch must be set to neutral to release a software lock before entering a new configuration on the command triad**.
This is intended to reduce the risk of inadvertently entering an incomplete or incorrect command.

## Administrative Functions
* (-1, -1, -1, -1): Reboot the BBB.
* (-1, 1, -1, 1): Poweroff the BBB.

## Static Tests
* (-1, 1, 1, 1): Start the cleaning system (brushes, conveyor, pump).
* (-1, 0, 0, 0): Stop the cleaning system (brushes, conveyor, pump).

## Dynamic Tests
### Reactive
* (-1, -1, 1, 1): Drive forward at 0.6m/s until an obstacle is detected 1.5m ahead of the LIDAR.

### Straight forward (fast, slow).
* (1, 1, 1, -1): Drive forward at 1m/s for 3s.
* (1, 1, 1, 0): Drive forward at 1m/s for 3s (with brushes, conveyor).
* (1, 1, 1, 1): Drive forward at 1m/s for 3s (with brushes, conveyor, pump).
* (1, 1, 0, -1): Drive forward at 0.3m/s for 9s.
* (1, 1, 0, 0): Drive forward at 0.3m/s for 9s (with brushes, conveyor).
* (1, 1, 0, 1): Drive forward at 0.3m/s for 9s (with brushes, conveyor, pump).

### Circular arc (large--small).
* (1, 1, -1, -1): Turn left at 0.3m/s forward around r=10m circle for 9s.
* (1, 1, -1, 0): Turn left at 0.3m/s forward around r=10m circle for 9s (with brushes, conveyor).
* (1, 1, -1, 1): Turn left at 0.3m/s forward around r=10m circle for 9s (with brushes, conveyor, pump).
* (1, 0, 1, -1): Turn left at 0.3m/s forward around r=5m circle for 9s.
* (1, 0, 1, 0): Turn left at 0.3m/s forward around r=5m circle for 9s (with brushes, conveyor).
* (1, 0, 1, 1): Turn left at 0.3m/s forward around r=5m circle for 9s (with brushes, conveyor, pump).
* (1, 0, 0, -1): Turn left at 45°/s around r=2m circle for 3s.
* (1, 0, 0, 0): Turn left at 0.3m/s around r=0.9m circle for 2s.

### Corners of a square (1, 4).
* (1, -1, 0, -1): Drive a 4 meter square and 1 corner left at 0.6m/s.
* (1, -1, 0, 0): Drive a 4 meter square and 1 corner left at 0.6m/s (with brushes, conveyor).
* (1, -1, 0, 1): Drive a 4 meter square and 1 corner left at 0.6m/s (with brushes, conveyor, pump).
* (1, -1, 1, -1): Drive a 4 meter square and 4 corners at 0.6m/s.
* (1, -1, 1, 0): Drive a 4 meter square and 4 corners at 0.6m/s (with brushes, conveyor).
* (1, -1, 1, 1): Drive a 4 meter square and 4 corners at 0.6m/s (with brushes, conveyor, pump).
