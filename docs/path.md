# Path Module Interface
Open loop path following (timer-based) can be accomplished with the [`Path`](../src/Navigate/Path/Path.py) module.
Its `path()` method implements a threaded sleep based control of the [`Drive`] (../src/Drive/Drive.py) module.

Its arguments are:

1. A list of tuples specifying a full `Drive.drive()` command and a time in seconds.
2. A function to run at the start of the path, e.g. to start the brushes.
3. A function to run at the end of the path.
4. Optionally, a delay in seconds before commencing (default: 10s).

The delay is present for safety reasons, so that the user may step back from the device before it starts.
Once a path begins, a new one cannot be entered until it finishes or is canceled (e.g. with its `stop()` method or by sensor interrupt).

Demonstration functions like those in the [demos](../src/demos.py) module are simply implemented as returning the drive command tuple list.
Future work may involve recasting the `Path` module to take input from a generator for real time path development by a navigation algorithm.
