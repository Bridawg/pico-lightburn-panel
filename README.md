# Pico LightBurn Panel

Wall-mounted button panel for triggering LightBurn laser cutter macros, using a Raspberry Pi Pico as a USB HID keyboard.

## Hardware

- Raspberry Pi Pico (original, micro USB)
- 5x 30mm arcade buttons (Green, Red, Yellow, Blue, Black)
- 1x 3-pin toggle switch (Home / Far corner)
- 1x 8mm green panel mount LED (power indicator)
- 1x 330Ω resistor
- Laser-cut box: 200×100×40mm, ply front + MDF body

## Wiring

| Component | GPIO |
|-----------|------|
| Green (Start) | GP15 |
| Red (Stop) | GP0 |
| Yellow (Frame) | GP7 |
| Blue (TBC) | GP4 |
| Black (TBC) | GP20 |
| Toggle (centre) | GND |
| Toggle (one outer pin) | GP12 |
| All button commons | GND |
| LED | 330Ω → 3V3 OUT (pin 36) → GND |

Toggle is SPDT: centre pin to GND, one outer pin to GP12. LOW = Home, HIGH = Far corner. Other outer pin unused.

Toggle: centre (common) → GND, outer pins → GP5 and GP6.

## LightBurn shortcuts

Assign these in LightBurn under **Edit → Settings → Hotkeys / Macro Buttons**:

| Shortcut | Button | Action |
|----------|--------|--------|
| Alt+S | Green | Start |
| Ctrl+Esc | Red | Stop |
| Ctrl+Shift+A | Yellow | Frame |
| F1 | Blue | (unassigned) |
| F2 | Black | (unassigned) |
| Ctrl+H | Toggle ON | Home |
| Ctrl+Shift+Alt+G | Toggle OFF | Move to far corner |

## Deploy

1. Install [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) on the Pico
2. Copy `adafruit_hid` library folder into `lib/` on the Pico drive
3. Copy `code.py` to the root of the Pico drive

## Box files

SVG files for laser cutting (all pieces sized for 3mm material unless adjusted):

- `lightburn_panel.svg` — front face (ply)
- `panel_back.svg` — back panel (MDF)
- `panel_top_rail.svg` — top rail (MDF)
- `panel_bottom_rail.svg` — bottom rail with USB cutout (MDF)
- `panel_sides_ribs.svg` — sides and internal ribs (MDF)
