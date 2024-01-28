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

capslock = all_pins[8]
micmute = all_pins[9]
fnlock = all_pins[10]
mute = all_pins[15]
leds = [capslock, fnlock, mute, micmute]
kbd_bl_pwm = all_pins[11]
hotkey = all_pins[14]
#kbd_bl_pwm.switch_to_output(False)

def test_leds():
    #p.switch_to_output(kbd_bl_pwm, True)
    for p in leds:
        p.switch_to_output(False)
        time.sleep(1)
        p.switch_to_input(pull=digitalio.Pull.UP)
    #p.switch_to_output(kbd_bl_pwm, False)

def test_hotkey():
    while True:
        fn_pressed = not hotkey.value
        #print(fn_pressed)
        print(all_pins[11].value, all_pins[14].value)
        time.sleep(0.5)
        #fnlock.switch_to_output(not fn_pressed)

#test_leds()
print("Here I am")
while True:
    for pin, d in all_pins.items():
        if pin == 24 or pin == 13: continue
        if d.value == False:
            print(pin, "low")
    time.sleep(0.25)
#test_hotkey()