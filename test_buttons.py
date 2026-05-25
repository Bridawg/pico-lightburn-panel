#!/usr/bin/env python3
"""
Test script for the LightBurn panel buttons.
Listens for keystrokes from the Pico and reports which button was pressed.
Run with: python3 test_buttons.py
"""

import evdev
from evdev import ecodes

DEVICE = '/dev/input/event15'  # Raspberry Pi Pico Keyboard

BUTTON_MAP = {
    frozenset(['KEY_LEFTALT', 'KEY_S']):                                    'GREEN  - Start',
    frozenset(['KEY_LEFTCTRL', 'KEY_ESC']):                                 'RED    - Stop',
    frozenset(['KEY_LEFTCTRL', 'KEY_LEFTSHIFT', 'KEY_LEFTALT', 'KEY_G']):  'YELLOW - Far corner',
    frozenset(['KEY_LEFTCTRL', 'KEY_LEFTSHIFT', 'KEY_A']):                  'BLUE   - Frame',
    frozenset(['KEY_F2']):                                                   'BLACK  - (unassigned)',
    frozenset(['KEY_LEFTCTRL', 'KEY_H']):                                   'TOGGLE - Home',
    frozenset(['KEY_LEFTCTRL', 'KEY_LEFTSHIFT', 'KEY_LEFTALT', 'KEY_G']):  'TOGGLE - Far corner',
}

MODIFIERS = {'KEY_LEFTCTRL', 'KEY_RIGHTCTRL', 'KEY_LEFTSHIFT', 'KEY_RIGHTSHIFT',
             'KEY_LEFTALT', 'KEY_RIGHTALT', 'KEY_LEFTMETA', 'KEY_RIGHTMETA'}

def main():
    try:
        dev = evdev.InputDevice(DEVICE)
    except PermissionError:
        print(f"Permission denied on {DEVICE} — try: sudo python3 test_buttons.py")
        return

    print(f"Listening on: {dev.name}")
    print("Press buttons on the panel (Ctrl+C to stop)...\n")

    held = set()

    for event in dev.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        key = ecodes.KEY[event.code]

        if event.value == 1:    # key down
            held.add(key)
        elif event.value == 0:  # key up
            combo = frozenset(held)
            label = BUTTON_MAP.get(combo)
            if label:
                print(f"  ✓ {label}")
            elif held and not combo.issubset(MODIFIERS):
                print(f"  ? Unknown combo: {sorted(held)}")
            held.discard(key)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
