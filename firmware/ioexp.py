# SPDX-FileCopyrightText: 2024 C. Scott Ananian
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Pin Map Script"""
import microcontroller
import board
import digitalio
import time
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

all_pins = dict()
for pin in dir(microcontroller.pin):
    p = getattr(microcontroller.pin, pin)
    if isinstance(p, microcontroller.Pin):
        num = int(pin[4:])
        if num >= 2:
            d = digitalio.DigitalInOut(p)
            d.switch_to_input(pull=digitalio.Pull.UP)
            all_pins[num] = d

i2c = busio.I2C(microcontroller.pin.GPIO1, microcontroller.pin.GPIO0)
ioexp_reset = all_pins[2]
ioexp_reset.switch_to_output(False)
time.sleep(0.1)
ioexp_reset.switch_to_output(True)
time.sleep(0.1)
mcp = MCP23017(i2c)

io_pins = dict()
for num in range(0,16):
    io_pins[num] = mcp.get_pin(num)
    io_pins[num].switch_to_input(pull=digitalio.Pull.UP)

capslock = all_pins[8]
micmute = all_pins[9]
fnlock = all_pins[10]
mute = all_pins[15]
leds = [capslock, fnlock, mute, micmute]
kbd_bl_pwm = all_pins[11]
hotkey = all_pins[14]

kbd_bl_pwm.switch_to_output(False)

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
        fnlock.switch_to_output(not fn_pressed)
        #print(fn_pressed)
        #print(all_pins[11].value, all_pins[14].value)
        time.sleep(0.5)

def test_inputs():
    while True:
        fnlock.switch_to_output(hotkey.value)
        for pin, d in all_pins.items():
            if pin == 24 or pin == 13 or pin == 11: continue
            if d.value == False:
                print(pin, "low")
        time.sleep(0.25)

def test_ioexp():
    io_pins[14].switch_to_output(False)
    test_inputs()

print("Here I am")
#test_leds()
#test_hotkey()
test_ioexp()