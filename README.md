# conway's game of life

group project for our data structures and algorithms class.  
we built conway's game of life with both:

- a text mode (terminal)
- a graphical mode using the `game2dboard` library

the project uses several data structures from class:
- 2d list for the grid
- queue (deque) for bfs
- stack for undo
- simple menu-based input
- bfs to find the largest live cell cluster

---

## 👥 group members

- student 1 — Gustave  
- student 2 — Fernando
- student 3 — Ana-Maria  
- student 4 — Felipe  

---

## 📁 project structure

```text
conway_game_of_life/
├─ main.py              # entry point
├─ config.py            # grid size and symbols
├─ game_logic.py        # game rules and bfs
├─ patterns.py          # glider & small exploder patterns
├─ ui_text.py           # text/terminal mode
├─ ui_board.py          # game2dboard graphical mode
├─ README.md
└─ requirements.txt
