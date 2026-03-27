import os
import pytest

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorCLI
from maze.maze_game import GameRunner


# --------------------------------------------------
# Helpers
# --------------------------------------------------

class DummySolution:
    teamname = "dummy"

    def __init__(self):
        pass

    def get_step(self, cell):
        # Always try right, otherwise down
        if not cell["walls"]["right"]:
            return "right"
        if not cell["walls"]["bottom"]:
            return "bottom"
        if not cell["walls"]["top"]:
            return "top"
        return "left"


class BadSolution:
    teamname = "bad"

    def get_step(self, cell):
        return "invalid_direction"


class WallCrashSolution:
    teamname = "crash"

    def get_step(self, cell):
        return "top"  # often invalid (wall)

class FullSolution:
    teamname = "reference"

    def __init__(self):
        # Internal map: (r,c) -> walls
        self.map = {}

        # Path tracking
        self.path_stack = []
        self.visited = set()

        # Position tracking (relative)
        self.pos = (0, 0)

        # Known target
        self.target = None

        # Phase handling
        self.phase = "explore"

        # Precomputed paths
        self.return_path = []
        self.fast_path = []

    # ----------------------------------------
    # Helpers
    # ----------------------------------------

    DIRS = ["top", "right", "bottom", "left"]

    VECTORS = {
        "top": (-1, 0),
        "right": (0, 1),
        "bottom": (1, 0),
        "left": (0, -1),
    }

    OPPOSITE = {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left",
    }

    def move(self, pos, d):
        dr, dc = self.VECTORS[d]
        return (pos[0] + dr, pos[1] + dc)

    # ----------------------------------------
    # Core API
    # ----------------------------------------

    def get_step(self, cell):
        # Save map
        self.map[self.pos] = cell["walls"]

        if cell["target"]:
            self.target = self.pos

        if self.phase == "explore":
            return self._explore(cell)

        elif self.phase == "return":
            return self._follow_path(self.return_path)

        elif self.phase == "fast":
            return self._follow_path(self.fast_path)

    # ----------------------------------------
    # Phase 1: Explore
    # ----------------------------------------

    def _explore(self, cell):
        self.visited.add(self.pos)

        # Found target → switch to return
        if self.target is not None:
            self.phase = "return"
            self.return_path = list(reversed(self.path_stack))
            return self._follow_path(self.return_path)

        # Try unexplored neighbors
        for d in self.DIRS:
            if not cell["walls"][d]:
                nxt = self.move(self.pos, d)
                if nxt not in self.visited:
                    self.path_stack.append(self.OPPOSITE[d])
                    self.pos = nxt
                    return d

        # Backtrack
        if self.path_stack:
            d = self.path_stack.pop()
            self.pos = self.move(self.pos, d)
            return d

        # Should not happen
        return "top"

    # ----------------------------------------
    # Follow precomputed path
    # ----------------------------------------

    def _follow_path(self, path):
        if not path:
            # Phase transitions
            if self.phase == "return":
                self.phase = "fast"
                self.fast_path = self._compute_fastest_path()
                return self._follow_path(self.fast_path)

            return "top"

        d = path.pop(0)
        self.pos = self.move(self.pos, d)
        return d

    # ----------------------------------------
    # Fastest path (Dijkstra)
    # ----------------------------------------

    def _compute_fastest_path(self):
        import heapq

        start = (0, 0)
        target = self.target

        def cost(prev, curr):
            if prev is None:
                return 1
            if prev == curr:
                return 1
            if self.OPPOSITE[prev] == curr:
                return 4
            return 3

        heap = [(0, start, None)]
        best = {}
        parent = {}

        while heap:
            c, pos, prev = heapq.heappop(heap)

            state = (pos, prev)
            if state in best and best[state] <= c:
                continue

            best[state] = c

            if pos == target:
                return self._reconstruct(parent, state)

            if pos not in self.map:
                continue

            walls = self.map[pos]

            for d in self.DIRS:
                if walls[d]:
                    continue

                nxt = self.move(pos, d)
                nc = c + cost(prev, d)

                nstate = (nxt, d)

                if nstate in best and best[nstate] <= nc:
                    continue

                parent[nstate] = state
                heapq.heappush(heap, (nc, nxt, d))

        return []

    def _reconstruct(self, parent, state):
        path = []

        while state in parent:
            (pos, d) = state
            path.append(d)
            state = parent[state]

        return list(reversed(path))
    
# --------------------------------------------------
# Basic movement
# --------------------------------------------------

def test_step_moves_position():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, DummySolution)

    start = runner.pos
    runner.step("phase1")

    assert runner.pos != start


# --------------------------------------------------
# Invalid move handling
# --------------------------------------------------

def test_invalid_direction_raises():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, BadSolution)

    with pytest.raises(ValueError):
        runner.step("phase1")


def test_wall_collision_raises():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, WallCrashSolution)

    with pytest.raises(ValueError):
        runner.step("phase1")
        runner.step("phase1")

# --------------------------------------------------
# Tick cost behavior
# --------------------------------------------------

def test_tick_increases():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, DummySolution)

    initial_tick = runner.tick
    runner.step("phase1")

    assert runner.tick > initial_tick


# --------------------------------------------------
# Phase progression
# --------------------------------------------------

def test_run_completes_and_creates_file(tmp_path):
    maze = Maze(10, 10, MazeGeneratorCLI())
    maze.generate()

    os.chdir(tmp_path)

    runner = GameRunner(maze, FullSolution)
    result_file = runner.run()

    assert os.path.exists(result_file)


# --------------------------------------------------
# Output file format
# --------------------------------------------------

def test_output_file_format(tmp_path):
    maze = Maze(10, 10, MazeGeneratorCLI())
    maze.generate()

    os.chdir(tmp_path)

    runner = GameRunner(maze, FullSolution)
    result_file = runner.run()

    with open(result_file, "r") as f:
        lines = f.readlines()

    # First line = scores
    first = lines[0].strip().split(",")
    assert len(first) == 2

    # Remaining lines = moves
    for line in lines[1:]:
        parts = line.strip().split(",")
        assert len(parts) == 4


# --------------------------------------------------
# Timeout behavior
# --------------------------------------------------

def test_timeout_stops_run():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, DummySolution)

    result_file = runner.run()

    # Should still produce output even if incomplete
    assert result_file is not None


# --------------------------------------------------
# History recording
# --------------------------------------------------

def test_history_records_moves():
    maze = Maze(5, 5, MazeGeneratorCLI())
    maze.generate()

    runner = GameRunner(maze, DummySolution)
    runner.step("phase1")

    assert len(runner.history) == 1

    tick, r, c, phase = runner.history[0]

    assert isinstance(tick, int)
    assert isinstance(r, int)
    assert isinstance(c, int)
    assert phase == "phase1"