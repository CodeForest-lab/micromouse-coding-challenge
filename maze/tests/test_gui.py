import tkinter as tk

from maze.maze_core import Maze
from maze.maze_generators import MazeGeneratorGUI
from maze.maze_gui import MazeGUI


def gui_test():
    config = {
        "loops" : False,
        "target" : None,
        "start" : None,
    }
    maze = Maze(20, 20, MazeGeneratorGUI(config))
    maze.generate()


    root = tk.Tk()
    MazeGUI(root, maze)
    root.mainloop()

if __name__ == "__main__":
    gui_test()