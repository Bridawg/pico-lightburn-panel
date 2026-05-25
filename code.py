import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

kbd = Keyboard(usb_hid.devices)

# --- Button setup ---
button_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4]
button_keys = [
    (Keycode.CONTROL, Keycode.F1),  # Green  - Start
    (Keycode.CONTROL, Keycode.F2),  # Red    - Stop
    (Keycode.CONTROL, Keycode.F3),  # Yellow - Frame
    (Keycode.CONTROL, Keycode.F4),  # Blue   - TBC
    (Keycode.CONTROL, Keycode.F5),  # Black  - TBC
]

buttons = []
for pin in button_pins:
    b = digitalio.DigitalInOut(pin)
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    buttons.append(b)

button_states = [True] * len(buttons)

# --- Toggle setup ---
toggle_a = digitalio.DigitalInOut(board.GP5)  # Home side
toggle_a.direction = digitalio.Direction.INPUT
toggle_a.pull = digitalio.Pull.UP

toggle_b = digitalio.DigitalInOut(board.GP6)  # Far corner side
toggle_b.direction = digitalio.Direction.INPUT
toggle_b.pull = digitalio.Pull.UP

last_toggle = None

# --- Main loop ---
while True:

    # Momentary buttons - fire on press, debounce on release
    for i, btn in enumerate(buttons):
        if not btn.value and button_states[i]:      # pressed
            kbd.send(*button_keys[i])
            button_states[i] = False
        elif btn.value and not button_states[i]:    # released
            button_states[i] = True

    # Toggle - fire on state change only
    if not toggle_a.value:
        toggle_state = "home"
    elif not toggle_b.value:
        toggle_state = "far"
    else:
        toggle_state = None

    if toggle_state and toggle_state != last_toggle:
        if toggle_state == "home":
            kbd.send(Keycode.CONTROL, Keycode.F6)   # Home macro
        else:
            kbd.send(Keycode.CONTROL, Keycode.F7)   # Far corner macro
        last_toggle = toggle_state

    time.sleep(0.01)  # 10ms debounce
