# ui_board.py

from tkinter import Frame, Label, Canvas, HORIZONTAL, LEFT, RIGHT, TOP, BOTTOM, X
from tkinter import ttk
from game2dboard import Board
from config import WIDTH, HEIGHT
from game_logic import make_grid, step, largest_live_cluster_size, copy_grid
from patterns import add_glider, add_small_exploder


def get_lexicon_text():
    return (
        "cell: alive (black) or dead (white) | "
        "generation: one time step | "
        "cluster: connected live cells | "
        "rules: live cell survives with 2-3 neighbors, dead cell born with exactly 3"
    )


def run_game2dboard_mode(grid=None, max_generations=0):
    board = Board(HEIGHT, WIDTH)
    board.title = "conway's game of life"
    board.cell_size = 15
    board.margin = 5
    board.grid_color = "#e0e0e0"
    board.cell_color = "white"

    state = {
        "grid": grid if grid else make_grid(randomize=False),
        "generation": 0,
        "max_generations": max_generations,
        "undo_stack": [],
        "running": False,
        "speed": 200
    }

    def refresh():
        g = state["grid"]
        for y in range(HEIGHT):
            for x in range(WIDTH):
                board._cells[y][x].bgcolor = "black" if g[y][x] == 1 else "white"

        largest_cluster = largest_live_cluster_size(g)
        gen = state["generation"]
        mg = state["max_generations"]

        status = f"gen {gen}"
        if mg > 0:
            status += f"/{mg}"
        status += f" | cluster: {largest_cluster} | speed: {state['speed']}ms"
        board.print(status)
        gen_label.config(text=f"Generation: {gen}")

    def step_once():
        if state["max_generations"] > 0 and state["generation"] >= state["max_generations"]:
            state["running"] = False
            board.stop_timer()
            play_btn.config(text="▶ Play")
            return

        state["undo_stack"].append(copy_grid(state["grid"]))
        state["grid"] = step(state["grid"])
        state["generation"] += 1
        refresh()

    def reset_grid(pattern="empty"):
        state["running"] = False
        board.stop_timer()
        play_btn.config(text="▶ Play")
        state["generation"] = 0
        state["undo_stack"] = []

        if pattern == "random":
            state["grid"] = make_grid(randomize=True)
        else:
            state["grid"] = make_grid(randomize=False)
            if pattern == "glider":
                add_glider(state["grid"])
            elif pattern == "exploder":
                add_small_exploder(state["grid"])
        refresh()

    def toggle_play():
        if state["running"]:
            state["running"] = False
            board.stop_timer()
            play_btn.config(text="▶ Play")
        else:
            state["running"] = True
            board.start_timer(state["speed"])
            play_btn.config(text="⏸ Pause")

    def do_step():
        if not state["running"]:
            step_once()

    def do_undo():
        if state["undo_stack"] and not state["running"]:
            state["grid"] = state["undo_stack"].pop()
            state["generation"] = max(0, state["generation"] - 1)
            refresh()

    def on_speed_change(val):
        state["speed"] = int(float(val))
        if state["running"]:
            board.stop_timer()
            board.start_timer(state["speed"])

    def on_max_gen_change(val):
        state["max_generations"] = int(float(val))

    def on_timer():
        if state["running"]:
            step_once()
        else:
            board.stop_timer()

    def on_mouse_click(btn, row, col):
        if not state["running"]:
            g = state["grid"]
            g[row][col] = 0 if g[row][col] == 1 else 1
            refresh()

    def on_key_press(key):
        key = key.lower()
        if key == "space":
            do_step()
        elif key == "a":
            toggle_play()
        elif key == "u":
            do_undo()
        elif key == "r":
            reset_grid("random")
        elif key == "q":
            board.close()

    def on_start():
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Dark.TFrame", background="#2a2a2a")
        style.configure("Dark.TLabel", background="#2a2a2a", foreground="white", 
                        font=("Helvetica", 11))
        style.configure("Small.TLabel", background="#2a2a2a", foreground="#888888", 
                        font=("Helvetica", 10))
        
        style.configure("TButton", font=("Helvetica", 10), padding=(12, 6))
        style.map("TButton",
                  background=[("active", "#555555"), ("!active", "#404040")],
                  foreground=[("active", "white"), ("!active", "white")])
        
        style.configure("Play.TButton", font=("Helvetica", 10, "bold"), padding=(12, 6))
        style.map("Play.TButton",
                  background=[("active", "#3a9d5a"), ("!active", "#2d7d46")],
                  foreground=[("active", "white"), ("!active", "white")])
        
        style.configure("TScale", background="#2a2a2a", troughcolor="#555555")

        control_frame = ttk.Frame(board._root, style="Dark.TFrame", padding=(10, 8))
        control_frame.pack(side=TOP, fill=X, before=board._canvas)

        # pattern buttons
        pattern_frame = ttk.Frame(control_frame, style="Dark.TFrame")
        pattern_frame.pack(side=LEFT, padx=(0, 15))

        ttk.Label(pattern_frame, text="Pattern:", style="Dark.TLabel").pack(side=LEFT, padx=(0, 8))
        ttk.Button(pattern_frame, text="Random", 
                   command=lambda: reset_grid("random")).pack(side=LEFT, padx=2)
        ttk.Button(pattern_frame, text="Empty", 
                   command=lambda: reset_grid("empty")).pack(side=LEFT, padx=2)
        ttk.Button(pattern_frame, text="Glider", 
                   command=lambda: reset_grid("glider")).pack(side=LEFT, padx=2)
        ttk.Button(pattern_frame, text="Exploder", 
                   command=lambda: reset_grid("exploder")).pack(side=LEFT, padx=2)

        # control buttons
        ctrl_frame = ttk.Frame(control_frame, style="Dark.TFrame")
        ctrl_frame.pack(side=LEFT, padx=(0, 15))

        nonlocal play_btn
        play_btn = ttk.Button(ctrl_frame, text="▶ Play", command=toggle_play, style="Play.TButton")
        play_btn.pack(side=LEFT, padx=2)
        ttk.Button(ctrl_frame, text="Step", command=do_step).pack(side=LEFT, padx=2)
        ttk.Button(ctrl_frame, text="Undo", command=do_undo).pack(side=LEFT, padx=2)

        # sliders
        slider_frame = ttk.Frame(control_frame, style="Dark.TFrame")
        slider_frame.pack(side=LEFT, padx=(0, 15))

        ttk.Label(slider_frame, text="Speed:", style="Small.TLabel").pack(side=LEFT)
        speed_slider = ttk.Scale(slider_frame, from_=500, to=50, orient=HORIZONTAL,
                                  command=on_speed_change, length=80)
        speed_slider.set(state["speed"])
        speed_slider.pack(side=LEFT, padx=(4, 12))

        ttk.Label(slider_frame, text="Max Gen:", style="Small.TLabel").pack(side=LEFT)
        max_gen_slider = ttk.Scale(slider_frame, from_=0, to=1000, orient=HORIZONTAL,
                                    command=on_max_gen_change, length=80)
        max_gen_slider.set(state["max_generations"])
        max_gen_slider.pack(side=LEFT, padx=4)

        # generation counter
        nonlocal gen_label
        gen_label = ttk.Label(control_frame, text="Generation: 0", style="Dark.TLabel")
        gen_label.pack(side=RIGHT)

        # info bar
        info_frame = ttk.Frame(board._root, style="Dark.TFrame", padding=(10, 6))
        info_frame.pack(side=BOTTOM, fill=X)
        ttk.Label(info_frame, text=get_lexicon_text(), style="Small.TLabel").pack(side=LEFT)
        ttk.Label(info_frame, text="Click cells to toggle | Keys: Space, A, U, R, Q", 
                  style="Small.TLabel").pack(side=RIGHT)

        refresh()

    play_btn = None
    gen_label = None

    board.on_start = on_start
    board.on_timer = on_timer
    board.on_mouse_click = on_mouse_click
    board.on_key_press = on_key_press
    board.show()
