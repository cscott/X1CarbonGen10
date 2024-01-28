print("Starting")

import microcontroller
import board
import digitalio
import busio
import time
from adafruit_mcp230xx.mcp23017 import MCP23017

from keypad import Event as KeyEvent
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import Scanner
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.extensions.lock_status import LockStatus

i2c = busio.I2C(microcontroller.pin.GPIO1, microcontroller.pin.GPIO0)
ioexp_reset = digitalio.DigitalInOut(microcontroller.pin.GPIO2)
ioexp_reset.switch_to_output(False)
time.sleep(0.05)
ioexp_reset.switch_to_output(True)
time.sleep(0.05)
mcp = MCP23017(i2c)

class MyScanner(Scanner):
    def __init__(self):
        self.drv = [None] * 16
        for ionum, p in enumerate([
                11, 8, 10, 12, 9, 13, 15, 5,
                7, 6, 3, 1, 2, 4, 0, 14
        ]):
            self.drv[p] = mcp.get_pin(ionum)
            self.drv[p].switch_to_input(pull=digitalio.Pull.UP)
        self.sense = [None] * 8
        for ionum, p in enumerate([ 5, 0, 2, 1, 7, 4, 3, 6 ]):
            pin = getattr(microcontroller.pin, 'GPIO' + str(16 + ionum))
            self.sense[p] = digitalio.DigitalInOut(pin)
            self.sense[p].switch_to_input(pull=digitalio.Pull.UP)
        self.len_rows = len(self.drv)
        self.len_cols = len(self.sense)
        self._key_count = self.len_rows * self.len_cols
        initial_state_value = b'\x01'
        self.state = bytearray(initial_state_value) * self._key_count
        self.offset = 0

    @property
    def key_count(self):
        return self._key_count

    def scan_for_changes(self):
        '''
        Poll the matrix for changes and return either None (if nothing updated)
        or a bytearray (reused in later runs so copy this if you need the raw
        array itself for some crazy reason) consisting of (row, col, pressed)
        which are (int, int, bool)
        '''
        ba_idx = 0
        any_changed = False

        for oidx, opin in enumerate(self.drv):
            opin.switch_to_output(False)

            for iidx, ipin in enumerate(self.sense):
                # cast to int to avoid
                #
                # >>> xyz = bytearray(3)
                # >>> xyz[2] = True
                # Traceback (most recent call last):
                #   File "<stdin>", line 1, in <module>
                # OverflowError: value would overflow a 1 byte buffer
                #
                # I haven't dived too far into what causes this, but it's
                # almost certainly because bool types in Python aren't just
                # aliases to int values, but are proper pseudo-types
                new_val = int(ipin.value)
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    row = oidx
                    col = iidx

                    pressed = not new_val # active low
                    self.state[ba_idx] = new_val

                    any_changed = True
                    break

                ba_idx += 1

            opin.switch_to_input(pull=digitalio.Pull.UP)
            if any_changed:
                break

        if any_changed:
            key_number = self.len_cols * row + col + self.offset
            return KeyEvent(key_number, pressed)

class MyKeyboard(KMKKeyboard):
    def __init__(self):
        self.matrix = [
            MyScanner(),
            KeysScanner(
                pins=[ microcontroller.pin.GPIO14 ], # HOTKEY
                value_when_pressed = False,
                pull = True
            )
        ]
        self.keymap = [
            [
                # DRV0
                KC.GRAVE, KC.N1, KC.Q, KC.TAB, KC.A, KC.ESCAPE, KC.Z, KC.NO,
                # DRV1
                KC.F1, KC.N2, KC.W, KC.CAPSLOCK, KC.S, KC.NO, KC.X, KC.NO,
                # DRV2
                KC.F2, KC.N3, KC.E, KC.F3, KC.D, KC.F4, KC.C, KC.NO,
                # DRV3
                KC.N5, KC.N4, KC.R, KC.T, KC.F, KC.G, KC.V, KC.B,
                # DRV4
                KC.N6, KC.N7, KC.U, KC.Y, KC.J, KC.H, KC.M, KC.N,
                # DRV5
                KC.EQUAL, KC.N8, KC.I, KC.RBRACKET, KC.K, KC.F6, KC.COMMA, KC.NO,
                # DRV6
                KC.F8, KC.N9, KC.O, KC.F7, KC.L, KC.NO, KC.DOT, KC.NO,
                # DRV7
                KC.MINUS, KC.N0, KC.P, KC.LBRACKET, KC.SCOLON, KC.QUOTE, KC.NO, KC.SLASH,
                # DRV8
                KC.F9, KC.F10, KC.NO, KC.BSPACE, KC.BSLASH, KC.F5, KC.ENTER, KC.SPACE,
                # DRV9
                KC.INSERT, KC.F12, KC.NO, KC.LGUI, KC.NO, KC.NO, KC.NO, KC.RIGHT,
                # DRV10
                KC.DELETE, KC.F11, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.DOWN,
                # DRV11
                KC.PGUP, KC.PGDOWN, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
                # DRV12
                KC.HOME, KC.END, KC.NO, KC.NO, KC.NO, KC.UP, KC.NO, KC.LEFT,
                # DRV13
                KC.NO, KC.PSCREEN, KC.NO, KC.NO, KC.NO, KC.LALT, KC.NO, KC.RALT,
                # DRV14
                KC.NO, KC.NO, KC.NO, KC.LSHIFT, KC.NO, KC.NO, KC.RSHIFT, KC.NO,
                # DRV15
                KC.LCTRL, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.RCTRL, KC.NO
            ],
        ]

capslock = digitalio.DigitalInOut(microcontroller.pin.GPIO8)
capslock.switch_to_output(True)
class LEDLockStatus(LockStatus):
    def set_lock_leds(self):
        capslock.value = not self.get_caps_lock()
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)  # Critically important. Do not forget
        if self.report_updated:
            self.set_lock_leds()

keyboard = MyKeyboard()
keyboard.extensions.append(LEDLockStatus())

if __name__ == '__main__':
    keyboard.go()