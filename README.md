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
| Green (Start) | GP0 |
| Red (Stop) | GP1 |
| Yellow (Frame) | GP2 |
| Blue (TBC) | GP3 |
| Black (TBC) | GP4 |
| Toggle → Home | GP5 |
| Toggle → Far corner | GP6 |
| All button commons | GND |
| LED | 330Ω → 3V3 OUT (pin 36) → GND |

Toggle: centre (common) → GND, outer pins → GP5 and GP6.

## LightBurn shortcuts

Assign these in LightBurn under **Edit → Settings → Hotkeys / Macro Buttons**:

| Shortcut | Action | GCode |
|----------|--------|-------|
| Ctrl+F1 | Start | — |
| Ctrl+F2 | Stop | — |
| Ctrl+F3 | Frame | — |
| Ctrl+F4 | Blue (TBC) | — |
| Ctrl+F5 | Black (TBC) | — |
| Ctrl+F6 | Home | `G21 G28` |
| Ctrl+F7 | Far corner | `G21 G0 X400 Y415` |

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
