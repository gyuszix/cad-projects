# E-ink Weather Station Case

A 3D-printable case and lift-off lid for a WeAct 2.9-inch e-paper display, an ESP32 on a half-size breadboard, an 802540 LiPo battery, and a TP4056 USB-C charger.

The parts are made by resizing the original "ESP32 + ePaper-Display" case and lid (`build123d_sources/`) with [build123d](https://github.com/gumyr/build123d), adding breadboard support rails, and cutting a USB-C opening.

## Pictures

**Fit preview:** plan and section views showing how the components fit.

![Fit preview](Epaper_Enclosure_2p9_Preview.png)

**Original vs adapted:** the original case next to the resized version.

![Original vs adapted](Epaper_Original_vs_Adapted.png)

## Files

| File | What it is |
| --- | --- |
| `Build123d_Enclosure.py` | Generator script. Builds the case and lid. |
| `build123d_sources/` | The original case and lid STLs. The script needs these as input. |
| `build123d_generated/` | Output: `Epaper_Case_2p9.stl` and `Epaper_Lid_2p9.stl`. |
| `*.png` | Fit preview and a comparison of the original and adapted case. |

## Dimensions

All dimensions are in millimeters.

**Enclosure**
- Outer footprint: 100 × 67
- Case base height: 51.6. Lid top: 53.2.
- Floor thickness: 1.5 (kept from the original). Only the walls are stretched in height.
- The lid keeps the original lid thickness and is resized to the new footprint.

**Breadboard support**
- Rail frame: 82.6 × 55.0, rails 3.5 wide and 2.0 tall
- The breadboard rests on the rails at z = 10.2–12.2.

**USB-C charger opening**
- 13.0 × 5.6, centered on the short front wall, center at z = 4.6

**Internal fit**
- Lower bay (under the breadboard) fits an 802540 battery (42 × 25.5 × 8.2) and a TP4056 USB-C board (about 28 × 17 × 4).
- Display: WeAct 2.9-inch module, 91.8 × 37.5, active area 66.89 × 29.05. It mounts under the lid.
- Tallest component stack: 50 from the case floor, including the breadboard and the display PCB under the lid.
- Jumper wires should stay below z = 45. The display PCB underside is at z = 48, which leaves 3 of clearance.

## Generating the STLs

1. Install Python 3.10 or newer, then create a virtual environment and install build123d:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install build123d
   ```

   (This repo already has a venv one level up, so you can use `../venv/bin/python` instead.)

2. Run the generator from this folder:

   ```sh
   python Build123d_Enclosure.py
   ```

3. The STLs are written to `build123d_generated/`:
   - `Epaper_Case_2p9.stl`
   - `Epaper_Lid_2p9.stl`

To change the size, edit the constants at the top of `Build123d_Enclosure.py` (`TARGET_X`, `TARGET_Y`, `CASE_TOP`, and the `PORT_*` values) and run it again. The breadboard rail sizes are in `make_case()`.

## Printing

Load both STLs from `build123d_generated/` into your slicer and print them as separate parts.

Before you print a final version, measure your actual parts. The dimensions above use common catalog sizes, and breadboards and TP4056 boards vary by manufacturer. A quick test print of the case's lower section is a cheap way to check the USB-C opening and the battery bay.

## Notes

- "TA4056" in the original parts list is treated as a TP4056 USB-C charger module.
- The output is mesh-based, because it is built from the original STLs, so it may be retessellated compared with the source files.
- The repo's `.gitignore` ignores `*.stl`. To commit the source meshes the script needs, add `!e-ink-weather-station-case/build123d_sources/*.stl` to it.
