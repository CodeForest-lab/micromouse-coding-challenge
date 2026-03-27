import os
import pytest

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorCLI, GeneratorConfig
from maze.maze_game import GameRunner


# Import your advanced/reference solution
from maze.tests.test_maze_game import FullSolution


# --------------------------------------------------
# Helper
# --------------------------------------------------

def parse_result(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    score1, score2 = map(int, lines[0].strip().split(","))

    phases = set()
    for line in lines[1:]:
        _, _, _, phase = line.strip().split(",")
        phases.add(phase)

    return score1, score2, phases


# --------------------------------------------------
# Parametrized test over sizes
# --------------------------------------------------

@pytest.mark.parametrize("rows,cols", [
    (5, 5),
    (10, 10),
    (20, 20),
    (50, 50),
    (50, 20),
    (20, 70),
    (100, 100),
])
def test_full_solution_completes_all_phases(tmp_path, rows, cols):
    os.chdir(tmp_path)

    config = GeneratorConfig(loops=True)
    maze = Maze(rows, cols, MazeGeneratorCLI(config))
    maze.generate()

    runner = GameRunner(maze, FullSolution)
    result_file = runner.run()

    score1, score2, phases = parse_result(result_file)

    # ✅ Both phases must have scores
    assert score1 != -1
    assert score2 != -1

    # ✅ All phases must be present
    assert "phase1" in phases
    assert "return" in phases
    assert "phase2" in phases