# game_logic.py

import random
from collections import deque
from config import WIDTH, HEIGHT

# build and copy grid

def make_grid(randomize=True):
    # build a height x width grid
    # time: o(h * w)
    # space: o(h * w)
    grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            if randomize:
                cell = 1 if random.random() < 0.25 else 0
            else:
                cell = 0
            row.append(cell)
        grid.append(row)
    return grid


def copy_grid(grid):
    # copy every cell of the grid once
    # time: o(h * w)
    # space: o(h * w)
    return [row[:] for row in grid]


# game rules

def count_neighbors(grid, x, y):
    # count alive neighbors around cell (x, y) with wrap-around edges
    # always checks 8 neighbors
    # time: o(1)
    # space: o(1)
    neighbors = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # skip the cell itself
            nx = (x + dx) % WIDTH
            ny = (y + dy) % HEIGHT
            neighbors += grid[ny][nx]
    return neighbors


def step(grid):
    # compute next generation from the current grid
    # visit every cell once and do o(1) work per cell
    # time: o(h * w)
    # space: o(h * w) for the new grid
    new_grid = []
    for y in range(HEIGHT):
        new_row = []
        for x in range(WIDTH):
            alive = grid[y][x] == 1
            neighbors = count_neighbors(grid, x, y)

            if alive:
                # live cell stays alive with 2 or 3 neighbors
                if neighbors == 2 or neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)
            else:
                # dead cell becomes live with exactly 3 neighbors
                if neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)
        new_grid.append(new_row)
    return new_grid


def largest_live_cluster_size(grid):
    # find size of biggest group of connected live cells
    # use bfs over the grid
    # let n = h * w
    # time: o(n)
    # space: o(n)
    visited = [[False] * WIDTH for _ in range(HEIGHT)]
    max_size = 0

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == 1 and not visited[y][x]:
                queue = deque()
                queue.append((y, x))
                visited[y][x] = True
                current_size = 0

                while queue:
                    cy, cx = queue.popleft()
                    current_size += 1

                    # explore 8 neighbors with wrap-around
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue
                            ny = (cy + dy) % HEIGHT
                            nx = (cx + dx) % WIDTH

                            if grid[ny][nx] == 1 and not visited[ny][nx]:
                                visited[ny][nx] = True
                                queue.append((ny, nx))

                if current_size > max_size:
                    max_size = current_size

    return max_size
