import pytest

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorCLI, GeneratorConfig
from maze.maze_tools import shortest_path, fastest_path, path_cost, generate_until_interesting


@pytest.fixture
def maze():
    config = GeneratorConfig(loops=False)
    generator = MazeGeneratorCLI(config)
    m = Maze(10, 10, generator)
    m.generate()
    return m

def test_shortest_paths_exist(maze):
    sp = shortest_path(maze)

    assert len(sp) > 0

def test_fastest_paths_exist(maze):
    fp = fastest_path(maze)

    assert len(fp) > 0

def test_fastest_path_has_valid_cost(maze):
    fp = fastest_path(maze)

    assert len(fp) > 0
    assert path_cost(fp) > 0

@pytest.mark.parametrize("size", [(5,5), (10,10), (20,20), (40,40), (100,100)])
def test_fastest_vs_shortest(size):
    rows, cols = size
    config = GeneratorConfig(loops=False)
    generator = MazeGeneratorCLI(config)
    maze = Maze(rows, cols, generator)
    maze.generate()

    sp = shortest_path(maze)
    fp = fastest_path(maze)

    assert path_cost(fp) <= path_cost(sp)

@pytest.mark.parametrize("size", [(5,5), (10,10), (20,20), (40,40), (100,100)])
def test_generate_until_interesting_loops(size):
    rows, cols = size
    config = GeneratorConfig(loops=True)
    generator = MazeGeneratorCLI(config)
    maze = Maze(rows, cols, generator)
    if (generate_until_interesting(maze)):
        sp = shortest_path(maze)
        fp = fastest_path(maze)
        
        assert path_cost(fp) < path_cost(sp)
    else:
        pytest.skip("Unable to generate an 'interesting' maze")
