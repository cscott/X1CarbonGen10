Basic firmware examples for initial bringup/testing, written
in Circuit Python.

First, install Circuit Python 8.x for the Adafruit KB2040 board,
which is close enough to our board to work.

Then copy the `lib` and `kmk` directories to
the `CIRCUITPY` drive.  These are from the "Adafruit CircuitPython
bundle 8.x" and from the "KMK" project.

Then we have a number of different examples to try; for each just
copy the file to `code.py` on the `CIRCUITPY` drive:
* `continuity.py`: a basic continuity tester which was helpful in
determining the initial keyboard matrix and keymap.
* `ledtest.py`: some code for testing the LEDs on the keyboard
* `ioexp.py`: some code for testing the IO expander
* `kmk.py`: A basic keyboard implementation in CircuitPython using
  KMK. No trackpoint support (a limitation of KMK), the Fn key is
  not currently mapped (this could be done), and the MUTE and MICMUTE
  LEDs are not supported (a limitation of KMK?).
