import tkinter as tk
from tkinter import messagebox

from maze.maze_io import save_maze 
from maze.maze_tools import generate_until_interesting


class MazeGUI:
    def __init__(self, root, maze, cell_size=25):
        self.root = root
        self.maze = maze
        self.cell_size = cell_size

        self.rows = maze.rows
        self.cols = maze.cols

        self.canvas = tk.Canvas(
            root,
            width=self.cols * cell_size,
            height=self.rows * cell_size,
            bg="white"
        )
        self.canvas.pack()

        # Optional control panel (only for GUI generator)
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        if self._is_gui_generator():
            self._build_controls()

        self.draw_base()
        self.draw_markers()

    # --------------------------------------------------
    # GENERATOR TYPE CHECK
    # --------------------------------------------------

    def _is_gui_generator(self):
        return self.maze.generator.__class__.__name__ == "MazeGeneratorGUI"

    # --------------------------------------------------
    # CONTROLS (only for GUI mode)
    # --------------------------------------------------

    def _build_controls(self):
        tk.Label(self.control_frame, text="GUI Generator").pack()

        # ---- LOOPS CHECKBOX ----
        self.loops_var = tk.BooleanVar(
            value=self.maze.generator.config.loops
        )

        tk.Checkbutton(
            self.control_frame,
            text="Allow loops",
            variable=self.loops_var
        ).pack()

        # ---- BUTTONS ----
        tk.Button(
            self.control_frame,
            text="Regenerate",
            command=self.regenerate
        ).pack()

        tk.Button(
            self.control_frame,
            text="Save Maze",
            command=self.save_maze_gui
        ).pack()

    def regenerate(self):
        self.maze.generator.config.loops = self.loops_var.get()
        generate_until_interesting(self.maze)
        self.draw_base()
        self.draw_markers()

    def save_maze_gui(self):
        try:
            folder = save_maze(self.maze, )
            messagebox.showinfo("Saved", f"Maze saved to {folder}/map.txt")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_phase_view(self, *_):
        self.draw_base()

        phase = self.phase_var.get()
        if hasattr(self, "paths") and phase in self.paths:
            self._draw_path(self.paths[phase], color="blue")

        self.draw_markers()

    # --------------------------------------------------
    # DRAWING
    # --------------------------------------------------

    def draw_base(self):
        self.canvas.delete("all")

        for r in range(self.rows):
            for c in range(self.cols):
                self._draw_cell(r, c)

    def draw_markers(self):
        self._draw_start()
        self._draw_target()

    def _draw_cell(self, r, c):
        cell = self.maze.get_cell(r, c)

        x = c * self.cell_size
        y = r * self.cell_size

        # Draw walls
        if cell.walls["top"]:
            self.canvas.create_line(x, y, x + self.cell_size, y)
        if cell.walls["right"]:
            self.canvas.create_line(
                x + self.cell_size, y,
                x + self.cell_size, y + self.cell_size
            )
        if cell.walls["bottom"]:
            self.canvas.create_line(
                x, y + self.cell_size,
                x + self.cell_size, y + self.cell_size
            )
        if cell.walls["left"]:
            self.canvas.create_line(x, y, x, y + self.cell_size)

    def _draw_path(self, path, color="orange"):
        for (r, c) in path:
            self._fill_cell(r, c, color)

    # --------------------------------------------------
    # START / TARGET
    # --------------------------------------------------

    def _draw_start(self):
        if not hasattr(self.maze, "start") or self.maze.start is None:
            return

        r, c = self.maze.start
        self._fill_cell(r, c, "green")

    def _draw_target(self):
        for (r, c) in self.maze.get_targets():
            self._fill_cell(r, c, "red")

    def _fill_cell(self, r, c, color):
        x = c * self.cell_size
        y = r * self.cell_size

        self.canvas.create_rectangle(
            x + 2, y + 2,
            x + self.cell_size - 2,
            y + self.cell_size - 2,
            fill=color,
            outline=""
        )

    # --------------------------------------------------
    # FUTURE: PATH DRAWING
    # --------------------------------------------------


    
    def set_paths(self, moves):
        self.paths = {
            "phase1": [],
            "return": [],
            "phase2": []
        }

        for _, r, c, phase in moves:
            self.paths[phase].append((r, c))

        self.phase_var = tk.StringVar(value="phase1")
        
        tk.Label(self.control_frame, text="View Phase").pack()

        tk.OptionMenu(
            self.control_frame,
            self.phase_var,
            "phase1", "return", "phase2",
            command=self.update_phase_view
        ).pack()

        self.update_phase_view()