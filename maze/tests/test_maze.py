import pytest
from collections import deque

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorCLI


# ---------- FIXTURE ----------

@pytest.fixture
def maze():
    generator = MazeGeneratorCLI(loops=False)
    m = Maze(10, 10, generator)
    m.generate()
    return m


# ---------- TESTS ----------

def test_start_exists(maze):
    assert maze.start is not None


def test_single_target(maze):
    targets = maze.get_targets()
    assert len(targets) == 1


def test_no_isolated_cells(maze):
    for r in range(maze.rows):
        for c in range(maze.cols):
            cell = maze.get_cell(r, c)
            assert not all(cell.walls.values()), f"Isolated cell at {(r, c)}"


def test_maze_connected(maze):
    visited = set()
    queue = deque([(0, 0)])

    while queue:
        r, c = queue.popleft()
        if (r, c) in visited:
            continue

        visited.add((r, c))
        cell = maze.get_cell(r, c)

        for direction in ["top", "right", "bottom", "left"]:
            if not cell.walls[direction]:
                nr, nc = maze.neighbor(r, c, direction)
                if maze.in_bounds(nr, nc):
                    queue.append((nr, nc))

    assert len(visited) == maze.rows * maze.cols


def test_target_reachable(maze):
    target = maze.get_targets()[0]

    visited = set()
    queue = deque([maze.start])

    while queue:
        r, c = queue.popleft()
        if (r, c) == target:
            return

        if (r, c) in visited:
            continue
        visited.add((r, c))

        cell = maze.get_cell(r, c)

        for direction in ["top", "right", "bottom", "left"]:
            if not cell.walls[direction]:
                nr, nc = maze.neighbor(r, c, direction)
                if maze.in_bounds(nr, nc):
                    queue.append((nr, nc))

    pytest.fail("Target is not reachable from start")


@pytest.mark.parametrize("size", [(5,5), (10,10), (20,20)])
def test_various_sizes(size):
    rows, cols = size
    generator = MazeGeneratorCLI()
    maze = Maze(rows, cols, generator)
    maze.generate()

    assert len(maze.get_targets()) == 1