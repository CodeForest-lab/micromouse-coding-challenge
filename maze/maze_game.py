import os

from maze.maze_tools import compute_cost, DIRECTIONS, DIR_VECTORS, OPPOSITE

class GameRunner:
    def __init__(self, maze, solution_class):
        self.maze = maze
        self.solution = solution_class()

        self.pos = maze.start
        self.dir = None

        self.tick = 0
        self.history = []  # (tick, r, c, phase)

        self.visited = set()

        self.max_steps = 2 * maze.rows * maze.cols
    

    def build_cell_view(self, r, c):
        cell = self.maze.get_cell(r, c)

        return {
            "walls": cell.walls.copy(),
            "target": cell.is_target
        }
    
    def step(self, phase):
        r, c = self.pos

        view = self.build_cell_view(r, c)

        move = self.solution.get_step(view)
        
        if move == "stop":
            print("Stop command recived!")
            return False

        if move not in DIRECTIONS:
            raise ValueError(f"Invalid move: {move}")
            return False

        if self.maze.get_cell(r, c).walls[move]:
            raise ValueError("Tried to walk through wall")
            return False

        dr, dc = DIR_VECTORS[move]
        nr, nc = r + dr, c + dc

        # cost
        cost = compute_cost(self.dir, move)
        self.tick += cost

        # update state
        self.pos = (nr, nc)
        self.dir = move
        self.visited.add((nr, nc))

        # record
        self.history.append((self.tick, nr, nc, phase))

        return True
    
    def run_phase(self, phase, stop_condition):
        steps = 0

        self.history.append((0, *self.pos, phase))

        while steps < self.max_steps:
            if stop_condition():
                return True

            if not self.step(phase):
                return False
            steps += 1

        return False  # timeout
    
    def run(self):
        start = self.maze.start
        target = list(self.maze.get_targets())[0]

        # ---------- PHASE 1 ----------
        reached = self.run_phase(
            "phase1",
            lambda: self.pos == target
        )

        score1 = self.tick if reached else None

        if not reached:
            return self.finish(score1, None)

        # ---------- RETURN ----------
        returned = self.run_phase(
            "return",
            lambda: self.pos == start
        )

        if not returned:
            return self.finish(score1, None)

        # reset direction for fair phase2
        self.dir = None

        # ---------- PHASE 2 ----------
        start_tick = self.tick

        reached2 = self.run_phase(
            "phase2",
            lambda: self.pos == target
        )

        score2 = self.tick - start_tick if reached2 else None

        return self.finish(score1, score2)
    
    def finish(self, score1, score2):
        team = getattr(self.solution, "teamname", "unknown")

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        if hasattr(self.maze.generator, "maze_dir"):
            output_dir = self.maze.generator.maze_dir

        filename = f"team_{team}.txt"
        file_path = os.path.join(output_dir, filename)
        print("file_path: ", file_path)
        with open(file_path, "w") as f:
            s1 = score1 if score1 is not None else -1
            s2 = score2 if score2 is not None else -1

            f.write(f"{s1},{s2}\n")

            for tick, r, c, phase in self.history:
                f.write(f"{tick},{r},{c},{phase}\n")

        return file_path