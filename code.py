"""
Arcade buttons -> USB HID keyboard for LightBurn.

Wiring (each input: GPIO pin -> switch -> GND, internal pull-up enabled):
  GP7  : button 1 (YELLOW)
  GP15 : button 2 (GREEN)
  GP0  : button 3 (RED)
  GP4  : button 4 (BLUE)
  GP20 : button 5 (BLACK)
  GP12 : toggle switch (center -> GND, one outer -> GP12)

How to edit a key:
  1. Find the line for the button in CONFIG below.
  2. Change the tuple of Keycode values.
     Single key:     (K.F1,)
     Chord:          (K.CONTROL, K.SHIFT, K.A)
     Letters / nums: K.A ... K.Z, K.ZERO ... K.NINE
     Modifiers:      K.CONTROL, K.SHIFT, K.ALT, K.GUI (=Win/Cmd)
     Specials:       K.ENTER, K.ESCAPE, K.SPACE, K.TAB, K.BACKSPACE
                     K.F1..K.F12, K.UP_ARROW, K.LEFT_ARROW, etc.
  3. Save. CircuitPython auto-reloads.

Full keycode list:
  https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode
"""

import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode as K


# =============================================================================
# CONFIG -- edit keys here
# =============================================================================

# pin                 keys (tuple)                  # color : function
BUTTON_1_PIN  = board.GP7
BUTTON_1_KEYS = (K.CONTROL, K.SHIFT, K.A)           # YELLOW : Frame laser

BUTTON_2_PIN  = board.GP15
BUTTON_2_KEYS = (K.ALT, K.S)                        # GREEN  : Start laser

BUTTON_3_PIN  = board.GP0
BUTTON_3_KEYS = (K.CONTROL, K.ESCAPE)               # RED    : Stop laser

BUTTON_4_PIN  = board.GP4
BUTTON_4_KEYS = (K.F1,)                             # BLUE   : (unassigned)

BUTTON_5_PIN  = board.GP20
BUTTON_5_KEYS = (K.F2,)                             # BLACK  : (unassigned)

TOGGLE_PIN      = board.GP12
TOGGLE_ON_KEYS  = (K.CONTROL, K.H)                  # toggle ON  : Home
TOGGLE_OFF_KEYS = (K.CONTROL, K.SHIFT, K.ALT, K.G)  # toggle OFF : Move opposite of home (macro)

DEBOUNCE_MS = 20
LED_FLASH_MS = 60  # onboard LED flash duration on each keypress

# =============================================================================
# Implementation -- no need to edit below
# =============================================================================

_BUTTONS = [
    (BUTTON_1_PIN, BUTTON_1_KEYS),
    (BUTTON_2_PIN, BUTTON_2_KEYS),
    (BUTTON_3_PIN, BUTTON_3_KEYS),
    (BUTTON_4_PIN, BUTTON_4_KEYS),
    (BUTTON_5_PIN, BUTTON_5_KEYS),
]

kbd = Keyboard(usb_hid.devices)

_led = digitalio.DigitalInOut(board.LED)
_led.direction = digitalio.Direction.OUTPUT
_led.value = False
_led_off_at = 0

def _flash():
    global _led_off_at
    _led.value = True
    _led_off_at = _now_ms() + LED_FLASH_MS

def _make_input(pin):
    p = digitalio.DigitalInOut(pin)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    return p

_btn_inputs = [(pin, keys, _make_input(pin)) for pin, keys in _BUTTONS]
_toggle = _make_input(TOGGLE_PIN)

_btn_state = [True] * len(_btn_inputs)
_btn_last  = [0] * len(_btn_inputs)
_tg_state  = _toggle.value
_tg_last   = 0

def _now_ms():
    return time.monotonic_ns() // 1_000_000

print("ready - 5 buttons + toggle armed")

while True:
    t = _now_ms()

    for i, (pin, keys, inp) in enumerate(_btn_inputs):
        v = inp.value
        if v != _btn_state[i] and (t - _btn_last[i]) > DEBOUNCE_MS:
            _btn_state[i] = v
            _btn_last[i] = t
            if not v:
                kbd.send(*keys)
                _flash()

    tv = _toggle.value
    if tv != _tg_state and (t - _tg_last) > DEBOUNCE_MS:
        _tg_state = tv
        _tg_last = t
        if tv:
            kbd.send(*TOGGLE_ON_KEYS)
        else:
            kbd.send(*TOGGLE_OFF_KEYS)
        _flash()

    if _led.value and t >= _led_off_at:
        _led.value = False

    time.sleep(0.005)
