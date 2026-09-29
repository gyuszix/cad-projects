"""Regenerate the adapted e-paper case and lid with build123d.

Requirements:
    pip install build123d

The two original STL inputs are kept in the sibling build123d_sources folder.
This script writes new files into build123d_generated so the existing deliverables
in this folder are not overwritten.

The original shapes are imported as triangulated STL geometry, then scaled and
modified. The script preserves that mesh-derived profile; it is not a clean-sheet
parametric reconstruction of the original CAD design.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    Keep,
    Mesher,
    Mode,
    Plane,
    Pos,
    add,
    export_stl,
    split,
)


HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE / "build123d_sources"
OUTPUT_DIR = HERE / "build123d_generated"
OUTPUT_DIR.mkdir(exist_ok=True)

SOURCE_CASE = SOURCE_DIR / "ESP32 + ePaper-Display Case.stl"
SOURCE_LID = SOURCE_DIR / "ESP32 + ePaper-Display Lid.stl"

# Adapted case dimensions and port opening, in millimeters.
TARGET_X = 100.0
TARGET_Y = 67.0
CASE_TOP = 51.6
ORIGINAL_X = 75.2
ORIGINAL_Y = 40.4
ORIGINAL_TOP = 15.0
ORIGINAL_FLOOR_TOP = 1.5
SX = TARGET_X / ORIGINAL_X
SY = TARGET_Y / ORIGINAL_Y
SZ = (CASE_TOP - ORIGINAL_FLOOR_TOP) / (ORIGINAL_TOP - ORIGINAL_FLOOR_TOP)

# The source Y limits are -20.6908607483 and +19.7091388702 mm.
CENTER_Y = (-20.6908607483 + 19.7091388702) * SY / 2
FRONT_Y = -34.31

PORT_WIDTH = 13.0
PORT_HEIGHT = 5.6
PORT_CENTER_Z = 4.6


def load_mesh(path: Path):
    """Load an STL as editable, faceted build123d geometry."""
    if not path.exists():
        raise FileNotFoundError(f"Required source STL not found: {path}")
    return Mesher().read(str(path))[0]


def cut_at_floor(mesh):
    """Split the source case at its 1.5 mm floor top plane."""
    with BuildPart() as lower_part:
        add(mesh)
        split(bisect_by=Plane.XY.offset(ORIGINAL_FLOOR_TOP), keep=Keep.BOTTOM)

    with BuildPart() as upper_part:
        add(mesh)
        split(bisect_by=Plane.XY.offset(ORIGINAL_FLOOR_TOP), keep=Keep.TOP)

    return lower_part.part, upper_part.part


def centered_box(x_size, y_size, z_size, center):
    """Create a box centered at an XYZ location."""
    return Pos(*center) * Box(
        x_size,
        y_size,
        z_size,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def make_case():
    source = load_mesh(SOURCE_CASE)
    lower, upper = cut_at_floor(source)

    # Keep the original bottom thickness; expand only the wall portion in Z.
    lower = lower.scale((SX, SY, 1.0), about=(0, 0, 0))
    upper = upper.scale((SX, SY, SZ), about=(0, 0, ORIGINAL_FLOOR_TOP))
    case = lower + upper

    # Half-size breadboard support frame. The ledges are fused into the case.
    bb_x, bb_y = 82.6, 55.0
    rail_z, rail_h, rail_w = 10.2, 2.0, 3.5
    rails = [
        centered_box(
            bb_x,
            rail_w,
            rail_h,
            (0, CENTER_Y - (bb_y / 2 - rail_w / 2), rail_z + rail_h / 2),
        ),
        centered_box(
            bb_x,
            rail_w,
            rail_h,
            (0, CENTER_Y + (bb_y / 2 - rail_w / 2), rail_z + rail_h / 2),
        ),
        centered_box(
            rail_w,
            bb_y,
            rail_h,
            (-(bb_x / 2 - rail_w / 2), CENTER_Y, rail_z + rail_h / 2),
        ),
        centered_box(
            rail_w,
            bb_y,
            rail_h,
            (+(bb_x / 2 - rail_w / 2), CENTER_Y, rail_z + rail_h / 2),
        ),
    ]
    for rail in rails:
        case = case + rail

    # Single USB-C cutout through the short front wall.
    cutter = centered_box(
        PORT_WIDTH,
        16.0,
        PORT_HEIGHT,
        (0, FRONT_Y + 1.0, PORT_CENTER_Z),
    )
    return case - cutter


def make_lid():
    lid = load_mesh(SOURCE_LID)
    lid = lid.scale((SX, SY, 1.0), about=(0, 0, 0))
    return Pos(0, 0, CASE_TOP - ORIGINAL_TOP) * lid


def main():
    case = make_case()
    lid = make_lid()

    case_path = OUTPUT_DIR / "Epaper_Case_2p9.stl"
    lid_path = OUTPUT_DIR / "Epaper_Lid_2p9.stl"
    export_stl(case, str(case_path), tolerance=0.01, angular_tolerance=0.1)
    export_stl(lid, str(lid_path), tolerance=0.01, angular_tolerance=0.1)

    print(f"Wrote {case_path}")
    print(f"Wrote {lid_path}")
    print(f"USB-C opening: {PORT_WIDTH:g} x {PORT_HEIGHT:g} mm")


if __name__ == "__main__":
    main()
