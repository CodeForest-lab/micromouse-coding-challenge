import random
from dataclasses import dataclass


@dataclass
class GeneratorConfig:
    loops: bool = False
    target: tuple[int] = None
    start: tuple[int] = None

class MazeGenerator:
    def generate(self, maze):
        raise NotImplementedError

# --------------------------------------------------
# CLI GENERATOR (Prim-based)
# --------------------------------------------------

class MazeGeneratorCLI(MazeGenerator):
    def __init__(self, config: GeneratorConfig = None):
        self.config = config if config else GeneratorConfig()

    def generate(self, maze):
        self.reset_visited(maze)

        rows, cols = maze.rows, maze.cols

        start_r = random.randint(0, rows - 1)
        start_c = random.randint(0, cols - 1)

        maze.get_cell(start_r, start_c).visited = True
        frontier = []

        self.add_frontier(maze, start_r, start_c, frontier)

        while frontier:
            row, col, direction = random.choice(frontier)
            frontier.remove((row, col, direction))

            nr, nc = maze.neighbor(row, col, direction)
            if not maze.in_bounds(nr, nc):
                continue

            current = maze.get_cell(row, col)
            neighbor = maze.get_cell(nr, nc)

            if current.visited ^ neighbor.visited:
                maze.remove_wall(row, col, direction)

                new_r, new_c = (nr, nc) if not neighbor.visited else (row, col)
                maze.get_cell(new_r, new_c).visited = True
                self.add_frontier(maze, new_r, new_c, frontier)

        # Optional loops
        if self.config.loops:
            self.add_loops(maze)

        # Set target + start
        self.set_start_and_target(maze)

    # ---------- HELPERS ----------

    def add_frontier(self, maze, row, col, frontier):
        for direction in ["top", "right", "bottom", "left"]:
            nr, nc = maze.neighbor(row, col, direction)
            if maze.in_bounds(nr, nc):
                if not maze.get_cell(nr, nc).visited:
                    frontier.append((row, col, direction))

    def add_loops(self, maze, chance=0.08):
        for r in range(maze.rows):
            for c in range(maze.cols):
                for direction in ["right", "bottom"]:
                    if random.random() < chance:
                        nr, nc = maze.neighbor(r, c, direction)
                        if maze.in_bounds(nr, nc):
                            maze.remove_wall(r, c, direction)

    def set_start_and_target(self, maze):
        rows, cols = maze.rows, maze.cols

        # Start
        if self.config.start:
            maze.start = self.config.start
        else:
            maze.start = random.choice([
                (0, 0),
                (0, cols - 1),
                (rows - 1, 0),
                (rows - 1, cols - 1)
            ])

        # Target
        if self.config.target:
            tr, tc = self.config.target
        else:
            tr, tc = rows // 2, cols // 2

        maze.set_target(tr, tc)

    def reset_visited(self, maze):
        for r in range(maze.rows):
            for c in range(maze.cols):
                maze.get_cell(r, c).visited = False


# --------------------------------------------------
# FROM FILE GENERATOR
# --------------------------------------------------

class MazeGeneratorFromFile(MazeGenerator):
    def __init__(self, grid_data):
        self.grid_data = grid_data

    def generate(self, maze):
        for r in range(maze.rows):
            for c in range(maze.cols):
                data = self.grid_data[r][c]

                cell = maze.get_cell(r, c)
                cell.walls = data["walls"]

                if data["target"]:
                    maze.set_target(r, c)

        # Start is undefined unless stored later
        maze.start = None


# --------------------------------------------------
# GUI GENERATOR (wrapper)
# --------------------------------------------------

class MazeGeneratorGUI(MazeGenerator):
    def __init__(self, config: GeneratorConfig = None):
        self.config = config if config else GeneratorConfig()

    def generate(self, maze):
        # Just reuse CLI generator logic
        generator = MazeGeneratorCLI(self.config)
        generator.generate(maze)