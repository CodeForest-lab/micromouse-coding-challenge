import pytest
import tkinter as tk

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorGUI, GeneratorConfig
from maze.maze_gui import MazeGUI

@pytest.fixture
def maze_gui():
    config = GeneratorConfig(loops=False)
    generator = MazeGeneratorGUI(config)
    m = Maze(10, 10, generator)
    m.generate()
    return m

def test_gui_create(maze_gui):
    root = tk.Tk()
    MazeGUI(root, maze_gui)

def manual_gui_test():
    maze = Maze(20, 20, MazeGeneratorGUI())
    maze.generate()

    root = tk.Tk()
    MazeGUI(root, maze)
    root.mainloop()

if __name__ == "__main__":
    manual_gui_test()