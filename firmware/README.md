Basic firmware examples for initial bring-up and testing, written
in Circuit Python.

First, install [Circuit Python 8.x for the Adafruit KB2040 board](https://circuitpython.org/downloads),
which is close enough hardware-wise to our board to work.

Then copy the `lib` and `kmk` directories from this directory to
the `CIRCUITPY` drive.  These are from the
[Adafruit CircuitPython bundle 8.x](https://circuitpython.org/libraries)
and from the
[KMK](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/Getting_Started.md)
project.

Then we have a number of different examples to try; for each just
copy the file to `code.py` on the `CIRCUITPY` drive:
* [`continuity.py`](./continuity.py):
  a basic continuity tester which was helpful in
  determining the initial keyboard matrix and keymap.
* [`ioexp.py`](./ioexp.py):
  some code for testing the IO expander and LEDs
* [`kmk.py`](./kmk.py):
  A basic keyboard implementation in CircuitPython using
  KMK. No trackpoint support (a limitation of KMK), the Fn key is
  not currently mapped (this could be done), and the MUTE and MICMUTE
  LEDs are not supported (a limitation of KMK?).
