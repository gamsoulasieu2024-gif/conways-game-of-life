from conway.config import WIDTH, HEIGHT


def add_small_exploder(grid):
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

