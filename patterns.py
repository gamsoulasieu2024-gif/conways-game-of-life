# patterns.py

from config import WIDTH, HEIGHT

def add_glider(grid):
    # place a glider near the center
    # touches 5 cells
    # time: o(1)
    # space: o(1)
    mid_y = HEIGHT // 2
    mid_x = WIDTH // 2

    coords = [
        (mid_y,     mid_x + 1),
        (mid_y + 1, mid_x + 2),
        (mid_y + 2, mid_x),
        (mid_y + 2, mid_x + 1),
        (mid_y + 2, mid_x + 2),
    ]

    for y, x in coords:
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            grid[y][x] = 1


def add_small_exploder(grid):
    # place a small exploder near the center
    # touches 7 cells
    # time: o(1)
    # space: o(1)
    mid_y = HEIGHT // 2
    mid_x = WIDTH // 2

    coords = [
        (mid_y,     mid_x),
        (mid_y - 1, mid_x),
        (mid_y + 1, mid_x),
        (mid_y,     mid_x - 1),
        (mid_y,     mid_x + 1),
        (mid_y - 1, mid_x - 1),
        (mid_y - 1, mid_x + 1),
    ]

    for y, x in coords:
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            grid[y][x] = 1
