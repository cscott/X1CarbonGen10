# SPDX-FileCopyrightText: 2024 C. Scott Ananian
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board
import digitalio
import time

all_pins = dict()
for pin in dir(microcontroller.pin):
    p = getattr(microcontroller.pin, pin)
    if isinstance(p, microcontroller.Pin):
        d = digitalio.DigitalInOut(p)
        d.switch_to_input(pull=digitalio.Pull.UP)
        num = int(pin[4:])
        all_pins[num] = d


def check_one():
    # reset state for safety's sake
    for pin, d in all_pins.items():
        d.switch_to_input(pull=digitalio.Pull.UP)
    for pin, d in all_pins.items():
        # set just this pin high
        d.switch_to_output(False)
        for pin2, d2 in all_pins.items():
            if pin > pin2 and d2.value == False:
                print(pin2, "connected to", pin)
        d.switch_to_input(pull=digitalio.Pull.UP)

while True:
    print("----")
    check_one()
    time.sleep(1)
