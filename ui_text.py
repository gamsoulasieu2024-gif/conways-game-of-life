# ui_text.py

import os
from config import WIDTH, HEIGHT, ALIVE, DEAD
from game_logic import (
    make_grid,
    copy_grid,
    step,
    largest_live_cluster_size,
)
from patterns import add_glider, add_small_exploder

# utils

def clear_screen():
    # clear the terminal screen
    # time: o(1)
    # space: o(1)
    os.system("cls" if os.name == "nt" else "clear")


def manual_edit(grid):
    # let the player add live cells by typing row,col pairs
    # let k be how many cells they add
    # time: o(k)
    # space: o(1)
    print("\nyou chose an empty grid.")
    print("now you can add live cells manually.")
    print(f"valid rows: 0 to {HEIGHT - 1}, valid cols: 0 to {WIDTH - 1}.")
    print("type coordinates as 'row,col' (without quotes).")
    print("press enter on an empty line when you are done.\n")

    while True:
        s = input("add live cell at (row,col) or press enter to finish: ").strip()
        if s == "":
            break
        try:
            row_str, col_str = s.split(",")
            r = int(row_str)
            c = int(col_str)
            if 0 <= r < HEIGHT and 0 <= c < WIDTH:
                grid[r][c] = 1
            else:
                print("out of bounds, try again.")
        except ValueError:
            print("invalid format, use row,col (ex: 5,10).")


def grid_to_string(grid, generation, largest_cluster=None, max_generations=None):
    # turn the grid into a multi-line string
    # one char per cell
    # time: o(h * w)
    # space: o(h * w)
    header = f"conway's game of life - generation {generation}"
    if max_generations and max_generations > 0:
        header += f"/{max_generations}"
    if largest_cluster is not None:
        header += f" | largest live cluster: {largest_cluster} cells"

    lines = [header]
    for y in range(HEIGHT):
        line = []
        for x in range(WIDTH):
            line.append(ALIVE if grid[y][x] == 1 else DEAD)
        lines.append("".join(line))
    return "\n".join(lines)


def get_lexicon_text():
    # return a fixed text that explains the terms
    # time: o(1)
    # space: o(1)
    return (
        "=== lexicon / info ===\n"
        "  • cell: each position in the grid (alive █ or dead ' ').\n"
        "  • generation: one time step when all cells update once.\n"
        "  • neighbour: any of the 8 cells around a given cell.\n"
        "  • rule:\n"
        "      - a live cell stays alive with 2 or 3 live neighbours.\n"
        "      - a dead cell becomes live with exactly 3 neighbours.\n"
        "  • cluster: group of live cells that touch (8 directions).\n"
        "  • largest cluster: size of the biggest live group in this step.\n"
        "  • patterns: random / glider / small exploder / manual edit.\n"
    )


def print_lexicon():
    # print the lexicon text to the terminal
    # time: o(1)
    # space: o(1)
    print(get_lexicon_text())


def run_text_mode(grid, max_generations):
    # main loop for text mode
    # for g generations, time: o(g * h * w)
    generation = 0
    undo_stack = []  # stack of previous grids for undo

    while True:
        clear_screen()
        largest_cluster = largest_live_cluster_size(grid)
        print(grid_to_string(grid, generation, largest_cluster, max_generations))

        print("\ncontrols:")
        print("  [enter] - next generation")
        print("  a       - auto-advance several generations")
        print("  u       - undo last generation")
        print("  l       - show lexicon / info")
        print("  q       - quit\n")

        if max_generations > 0 and generation >= max_generations:
            print("reached maximum number of generations.")
            break

        cmd = input("command [enter/a/u/l/q]: ").strip().lower()

        if cmd == "q":
            print("quitting simulation.")
            break
        elif cmd == "u":
            if undo_stack:
                grid = undo_stack.pop()
                generation = max(0, generation - 1)
            else:
                print("nothing to undo. press enter to continue.")
                input()
            continue
        elif cmd == "a":
            while True:
                steps_str = input("advance how many generations? ").strip()
                try:
                    steps = int(steps_str)
                    if steps <= 0:
                        print("please enter a positive integer.")
                        continue
                    break
                except ValueError:
                    print("please enter a valid integer.")

            for _ in range(steps):
                if max_generations > 0 and generation >= max_generations:
                    break
                undo_stack.append(copy_grid(grid))
                grid = step(grid)
                generation += 1
            continue
        elif cmd == "l":
            clear_screen()
            print_lexicon()
            input("press enter to return to the game...")
            continue
        else:
            if max_generations > 0 and generation >= max_generations:
                print("reached maximum number of generations.")
                break
            undo_stack.append(copy_grid(grid))
            grid = step(grid)
            generation += 1
