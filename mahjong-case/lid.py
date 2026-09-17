from build123d import *
from ocp_vscode import show

# ---- Tray being held (must match the tray script) ----
tray_l = 180.0   # tray length (long side)
tray_w = 109.0   # tray width

n_side = 2

clearance = 1.5
holder_wall = 5.0

lid_thickness = 3.0

interior_l = tray_l + 2 * clearance
interior_w = n_side * tray_w + 2 * clearance

outer_l = interior_l + 2 * holder_wall
outer_w = interior_w + 2 * holder_wall

with BuildPart() as lid:
    Box(outer_l, outer_w, lid_thickness)

show(lid)

export_stl(lid.part, "../tray_lid.stl")