
class Cell:
    def __init__(self):
        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }
        self.visited = False
        self.is_target = False


class Maze:
    def __init__(self, rows, cols, generator):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.start = None 
        self.generator = generator

    # ---------- GENERATION ----------

    def generate(self):
        if not self.generator:
            raise ValueError("MazeGenerator is required")

        self.reset_maze()
        self.generator.generate(self)

    def reset_maze(self):
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    # ---------- ACCESS HELPERS ----------

    def get_cell(self, row, col):
        return self.grid[row][col]

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbor(self, row, col, direction):
        if direction == "top":
            return row - 1, col
        if direction == "bottom":
            return row + 1, col
        if direction == "left":
            return row, col - 1
        if direction == "right":
            return row, col + 1
        return None, None

    def remove_wall(self, row, col, direction):
        nr, nc = self.neighbor(row, col, direction)

        if not self.in_bounds(nr, nc):
            return

        self.grid[row][col].walls[direction] = False

        opposite = {
            "top": "bottom",
            "bottom": "top",
            "left": "right",
            "right": "left"
        }

        self.grid[nr][nc].walls[opposite[direction]] = False

    # ---------- TARGET ----------

    def set_target(self, row, col):
        self.grid[row][col].is_target = True

    def get_targets(self):
        targets = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_target:
                    targets.append((r, c))
        return targets