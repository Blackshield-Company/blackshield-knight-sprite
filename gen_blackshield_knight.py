#!/usr/bin/env python3
"""Forge the blackshield-knight petdex spritesheet.

Atlas: 8 cols x 9 rows of 192x208 frames (1536x1872, Codex/petdex layout).
Rows: idle, running-right, running-left, waving, jumping, failed, waiting,
      running, review. 6 frames per state (cols 6-7 ignored by renderers).
Sprite grid: 24x26 cells at 8px each == 192x208 exactly.
"""
import json
from pathlib import Path
from PIL import Image

OUT_DIR = Path.home() / ".hermes" / "pets" / "blackshield-knight"
GRID_W, GRID_H, CELL = 24, 26, 8
COLS, ROWS = 8, 9

PAL = {
    "K": (27, 31, 40, 255),      # armor black
    "S": (143, 163, 189, 255),   # steel rim
    "s": (220, 229, 242, 255),   # bright steel
    "R": (224, 85, 95, 255),     # crimson
    "r": (142, 47, 56, 255),     # dark crimson
    "B": (13, 16, 23, 255),      # shield field
    "E": (255, 107, 114, 255),   # shield emblem crimson
    "W": (242, 246, 252, 255),   # gleam white
}


def blank():
    return [["." for _ in range(GRID_W)] for _ in range(GRID_H)]


def put(g, row, col, ch):
    if 0 <= row < GRID_H and 0 <= col < GRID_W:
        g[row][col] = ch


def span(g, row, c0, c1, ch):
    for c in range(c0, c1 + 1):
        put(g, row, c, ch)


def draw_body(g, *, plume_dx=0, plume_dy=0, plume_dark=False,
              eye="R", legs="stand", eye_dx=0, sword="up", gleam_row=None):
    P = "r" if plume_dark else "R"
    # plume
    span(g, 0 + plume_dy, 10 + plume_dx, 12 + plume_dx, P)
    span(g, 1 + plume_dy, 9 + plume_dx, 13 + plume_dx, P)
    span(g, 2 + plume_dy, 9 + plume_dx, 12 + plume_dx, P)
    # helmet
    span(g, 3, 9, 14, "K")
    put(g, 4, 8, "S"); span(g, 4, 9, 15, "K"); put(g, 4, 15, "S")
    put(g, 5, 8, "S"); put(g, 5, 9, "K")
    if eye == "X":  # dizzy
        put(g, 5, 10, "W"); put(g, 5, 13, "W")
    else:
        span(g, 5, 10 + eye_dx, 13 + eye_dx, eye)
    put(g, 5, 14, "K"); put(g, 5, 15, "S")
    put(g, 6, 8, "S"); span(g, 6, 9, 14, "K"); put(g, 6, 15, "S")
    span(g, 7, 9, 14, "K")
    # pauldrons + torso
    put(g, 8, 6, "S"); span(g, 8, 7, 16, "K"); put(g, 8, 17, "S")
    put(g, 9, 8, "S"); span(g, 9, 9, 14, "K"); put(g, 9, 15, "S")
    for r in (10, 11):
        put(g, r, 8, "S"); put(g, r, 9, "K"); put(g, r, 10, "K")
        put(g, r, 11, "r"); put(g, r, 12, "r")  # crimson tabard
        put(g, r, 13, "K"); put(g, r, 14, "K"); put(g, r, 15, "S")
    span(g, 12, 6, 7, "K"); span(g, 13, 6, 7, "K")  # sword arm (viewer's left)
    put(g, 12, 8, "S"); put(g, 12, 9, "K"); put(g, 12, 10, "K")
    put(g, 12, 11, "r"); put(g, 12, 12, "r")
    put(g, 12, 13, "K"); put(g, 12, 14, "K"); put(g, 12, 15, "S")
    put(g, 13, 8, "S"); span(g, 13, 9, 14, "K"); put(g, 13, 15, "S")
    # belt
    put(g, 14, 8, "S"); span(g, 14, 9, 14, "s"); put(g, 14, 15, "S")
    # legs + boots
    if legs == "stand":
        for r in range(15, 20):
            span(g, r, 9, 10, "K"); span(g, r, 13, 14, "K")
        span(g, 20, 8, 11, "K"); span(g, 20, 12, 15, "K")
        put(g, 20, 8, "S"); put(g, 20, 15, "S")
    elif legs == "scissor":
        for r in range(15, 20):
            span(g, r, 8, 9, "K"); span(g, r, 14, 15, "K")
        span(g, 20, 7, 10, "K"); span(g, 20, 13, 16, "K")
        put(g, 20, 7, "S"); put(g, 20, 16, "S")
    elif legs == "tuck":
        for r in range(15, 18):
            span(g, r, 9, 10, "K"); span(g, r, 13, 14, "K")
        span(g, 18, 8, 11, "K"); span(g, 18, 12, 15, "K")
        put(g, 18, 8, "S"); put(g, 18, 15, "S")
    # sword (viewer's left, held high)
    if sword == "up":
        put(g, 9, 5, "r")                      # grip
        span(g, 10, 4, 6, "S")                 # guard
        for r in range(4, 9):
            put(g, r, 5, "s")                  # raised blade
        put(g, 3, 5, "s")                      # tip
        if gleam_row is not None:
            put(g, gleam_row, 5, "W")


def draw_shield(g, *, dx=10, dy=0, gleam_col=None):
    """Black heater shield (viewer's right), steel rim, crimson cross."""
    span(g, 9 + dy, 14 + dx - 10, 19 + dx - 10, "S")
    put(g, 10 + dy, 4 + dx, "S"); span(g, 10 + dy, 5 + dx, 8 + dx, "B"); put(g, 10 + dy, 9 + dx, "S")
    put(g, 11 + dy, 4 + dx, "S"); put(g, 11 + dy, 5 + dx, "B")
    put(g, 11 + dy, 6 + dx, "E"); put(g, 11 + dy, 7 + dx, "E")
    put(g, 11 + dy, 8 + dx, "B"); put(g, 11 + dy, 9 + dx, "S")
    put(g, 12 + dy, 4 + dx, "S")
    span(g, 12 + dy, 5 + dx, 8 + dx, "E")  # cross horizontal bar
    put(g, 12 + dy, 9 + dx - 1, "S")
    put(g, 13 + dy, 4 + dx, "S"); put(g, 13 + dy, 5 + dx, "B")
    put(g, 13 + dy, 6 + dx, "E"); put(g, 13 + dy, 7 + dx, "E")
    put(g, 13 + dy, 8 + dx, "S")
    put(g, 14 + dy, 5 + dx, "S"); put(g, 14 + dy, 6 + dx, "B")
    put(g, 14 + dy, 7 + dx, "E"); put(g, 14 + dy, 8 + dx, "S")
    put(g, 15 + dy, 5 + dx, "S"); put(g, 15 + dy, 6 + dx, "E"); put(g, 15 + dy, 7 + dx, "S")
    put(g, 16 + dy, 6 + dx, "S")
    if gleam_col is not None:
        put(g, 10 + dy, gleam_col, "W")


def shift_y(g, dy):
    if dy == 0:
        return g
    out = blank()
    for r in range(GRID_H):
        for c in range(GRID_W):
            if g[r][c] != "." and 0 <= r + dy < GRID_H:
                out[r + dy][c] = g[r][c]
    return out


def mirror(g):
    return [list(reversed(row)) for row in g]


# ---- state frame builders (6 frames each) ----

def f_idle(i):
    variants = [
        dict(plume_dx=0),
        dict(plume_dx=1),
        dict(eye="r"),
        dict(plume_dx=-1),
        dict(plume_dx=0),
        dict(gleam_row=6),
    ]
    g = blank(); draw_body(g, **variants[i]); draw_shield(g)
    return g

def f_run(i):
    bob = (0, -1, 0, -1, 0, -1)[i]
    legs = "stand" if i % 2 == 0 else "scissor"
    g = blank(); draw_body(g, legs=legs); draw_shield(g, dy=bob)
    return shift_y(g, bob)

def f_wave(i):
    gleam = (5, None, 7, None, 5, None)[i]
    g = blank(); draw_body(g, sword="up", gleam_row=gleam); draw_shield(g)
    return g

def f_jump(i):
    dy = (0, -2, -4, -4, -2, 0)[i]
    g = blank(); draw_body(g, legs="tuck"); draw_shield(g)
    return shift_y(g, dy)

def f_failed(i):
    g = blank()
    draw_body(g, plume_dx=2, plume_dy=1, plume_dark=True, eye="X")
    draw_shield(g, dy=2)
    # dizzy stars
    stars_a = [(2, 6), (1, 17), (3, 5)]
    stars_b = [(1, 7), (2, 16), (0, 15)]
    for (r, c) in (stars_a if i % 2 == 0 else stars_b):
        put(g, r, c, "W" if (i // 2) % 2 == 0 else "R")
    return g

def f_waiting(i):
    bob = (0, 0, 1, 0, 0, 0)[i]
    eye_dx = (-1, -1, 0, 1, 1, 0)[i]
    g = blank(); draw_body(g, eye_dx=eye_dx); draw_shield(g, dx=11, dy=2)
    return shift_y(g, bob)

def f_review(i):
    gleam_col = (15, 16, 17, 18, 17, 16)[i]
    g = blank(); draw_body(g); draw_shield(g, dy=-3, gleam_col=gleam_col)
    return g


ROW_BUILDERS = [
    f_idle,
    f_run,
    lambda i: mirror(f_run(i)),   # running-left
    f_wave,
    f_jump,
    f_failed,
    f_waiting,
    f_run,                        # running (generic)
    f_review,
]

def render(grid):
    img = Image.new("RGBA", (GRID_W * CELL, GRID_H * CELL), (0, 0, 0, 0))
    px = img.load()
    for r in range(GRID_H):
        for c in range(GRID_W):
            ch = grid[r][c]
            if ch == ".":
                continue
            color = PAL[ch]
            for dy in range(CELL):
                for dx in range(CELL):
                    px[c * CELL + dx, r * CELL + dy] = color
    return img


def main():
    atlas = Image.new("RGBA", (COLS * 192, ROWS * 208), (0, 0, 0, 0))
    for row_i, builder in enumerate(ROW_BUILDERS):
        frames = [builder(i) for i in range(6)]
        frames += [frames[0], frames[1]]  # cols 6-7 ignored by renderers
        for col_i, grid in enumerate(frames):
            atlas.paste(render(grid), (col_i * 192, row_i * 208))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(OUT_DIR / "spritesheet.webp", format="WEBP", lossless=True,
               quality=100, method=6, exact=True)
    (OUT_DIR / "pet.json").write_text(json.dumps({
        "id": "blackshield-knight",
        "displayName": "Blackshield Knight",
        "description": "A sworn knight of the obsidian watch. Black heater shield, crimson plume, zero retreat.",
        "spritesheetPath": "spritesheet.webp",
        "createdBy": "generator",
    }, indent=2), encoding="utf-8")

    # Contact-sheet preview (all 9 rows x 6 used frames, 1x)
    preview = Image.new("RGBA", (6 * 192, 9 * 208), (20, 22, 30, 255))
    for row_i, builder in enumerate(ROW_BUILDERS):
        for col_i in range(6):
            preview.paste(render(builder(col_i)), (col_i * 192, row_i * 208))
    preview.save("/home/synth/blackshield-knight-preview.png")
    print("wrote", OUT_DIR / "spritesheet.webp", atlas.size)
    print("preview: /home/synth/blackshield-knight-preview.png")


if __name__ == "__main__":
    main()
