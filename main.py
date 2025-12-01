# main.py

from game_logic import make_grid
from patterns import add_glider, add_small_exploder
from ui_text import clear_screen, manual_edit, run_text_mode
from ui_board import run_game2dboard_mode

def main():
    # main entry point
    clear_screen()
    print("=== conway's game of life ===")
    print("choose starting pattern:")
    print("1) random")
    print("2) empty (you will manually add live cells)")
    print("3) glider")
    print("4) small exploder")

    choice = input("enter 1, 2, 3, or 4: ").strip()

    if choice == "1":
        grid = make_grid(randomize=True)
    else:
        grid = make_grid(randomize=False)

        if choice == "2":
            manual_edit(grid)
        elif choice == "3":
            add_glider(grid)
        elif choice == "4":
            add_small_exploder(grid)
        else:
            print("invalid choice, defaulting to empty grid.")
            manual_edit(grid)

    # ask for max generations
    while True:
        mg = input("max generations (0 for infinite): ").strip()
        try:
            max_generations = int(mg)
            if max_generations < 0:
                print("please enter 0 or a positive integer.")
                continue
            break
        except ValueError:
            print("please enter a valid integer.")

    # choose mode
    print("\nchoose mode:")
    print("1) text mode (ascii + controls)")
    print("2) graphical mode (game2dboard)")
    mode = input("enter 1 or 2: ").strip()

    if mode == "2":
        run_game2dboard_mode(grid, max_generations)
    else:
        run_text_mode(grid, max_generations)


if __name__ == "__main__":
    main()
