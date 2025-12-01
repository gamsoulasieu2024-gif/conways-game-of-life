# ui_board.py

from game2dboard import Board
from config import WIDTH, HEIGHT
from game_logic import step, largest_live_cluster_size, copy_grid
from ui_text import get_lexicon_text

def run_game2dboard_mode(grid, max_generations):
    # run game of life using game2dboard
    # let g be number of generations we simulate here
    # time: o(g * h * w)
    board = Board(HEIGHT, WIDTH)  # rows, columns

    board.title = "conway's game of life - game2dboard"
    board.cell_size = 15
    board.margin = 5
    board.grid_color = "#e0e0e0"
    board.cell_color = "white"

    # output bar at bottom for messages and lexicon text
    board.create_output(color="black", background_color="lightgray", font_size=12)

    # shared state
    state = {
        "grid": grid,
        "generation": 0,
        "max_generations": max_generations,
        "undo_stack": [],
        "running": False,        # auto-run flag
        "showing_lexicon": False # show or hide lexicon in output bar
    }

    def refresh():
        # update all board cells from the grid
        # time: o(h * w)
        g = state["grid"]
        gen = state["generation"]
        mg = state["max_generations"]

        for y in range(HEIGHT):
            for x in range(WIDTH):
                board[y][x] = "black" if g[y][x] == 1 else None

        largest_cluster = largest_live_cluster_size(g)

        header = f"gen {gen}"
        if mg and mg > 0:
            header += f"/{mg}"
        header += f" | largest cluster: {largest_cluster} cells"
        header += " | space: step  a: auto  u: undo  l: lexicon  q: quit"

        if state["showing_lexicon"]:
            board.print(get_lexicon_text() + "\n" + header)
        else:
            board.print(header)

    def step_once():
        # go forward one generation
        if state["max_generations"] > 0 and state["generation"] >= state["max_generations"]:
            board.print("reached maximum generations. press u to undo or q to quit.")
            state["running"] = False
            board.stop_timer()
            return

        state["undo_stack"].append(copy_grid(state["grid"]))
        state["grid"] = step(state["grid"])
        state["generation"] += 1
        refresh()

    def on_key_press(key: str):
        key = key.lower()
        if key == "space":
            step_once()
        elif key == "a":
            # toggle auto-run
            if state["running"]:
                state["running"] = False
                board.stop_timer()
                refresh()
            else:
                state["running"] = True
                board.start_timer(200)  # milliseconds
        elif key == "u":
            # undo last step
            if state["undo_stack"]:
                state["grid"] = state["undo_stack"].pop()
                state["generation"] = max(0, state["generation"] - 1)
                refresh()
            else:
                board.print("nothing to undo. press space to step or q to quit.")
        elif key == "l":
            # toggle lexicon display
            state["showing_lexicon"] = not state["showing_lexicon"]
            refresh()
        elif key == "q":
            board.close()

    def on_timer():
        # called by the timer when auto-run is on
        if state["running"]:
            step_once()
        else:
            board.stop_timer()

    def on_mouse_click(btn: int, row: int, col: int):
        # toggle cell with mouse only when not auto-running
        if state["running"]:
            return
        g = state["grid"]
        g[row][col] = 0 if g[row][col] == 1 else 1
        refresh()

    def on_start():
        # called once when board starts
        refresh()

    board.on_start = on_start
    board.on_key_press = on_key_press
    board.on_mouse_click = on_mouse_click
    board.on_timer = on_timer

    board.show()  # blocks until window is closed
