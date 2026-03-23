import os
import shutil

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorCLI
from maze.maze_io import save_maze, load_maze


def test_save_and_load(tmp_path="maze/tests"):
    # Create maze
    generator = MazeGeneratorCLI()
    maze = Maze(10, 10, generator)
    maze.generate()

    # Save
    folder_path = save_maze(maze, base_dir=tmp_path)

    file_path = os.path.join(folder_path, "map.txt")

    # Load
    rows, cols, gen = load_maze(file_path)

    loaded_maze = Maze(rows, cols, gen)
    loaded_maze.generate()

    # Compare structure
    for r in range(rows):
        for c in range(cols):
            original = maze.get_cell(r, c)
            loaded = loaded_maze.get_cell(r, c)

            assert original.walls == loaded.walls

    # Check target preserved
    assert maze.get_targets() == loaded_maze.get_targets()

    shutil.rmtree(folder_path)