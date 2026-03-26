import argparse
import os
import tkinter as tk

from maze.maze_core import Maze
from maze.maze_generators import (
    MazeGeneratorCLI,
    MazeGeneratorGUI,
    GeneratorConfig,
)
from maze.maze_io import save_maze, load_maze
from maze.maze_gui import MazeGUI


def parse_pair(value):
    if value is None:
        return None
    try:
        x, y = map(int, value.split(","))
        return x, y
    except:
        raise argparse.ArgumentTypeError("Expected format: x,y")


def corner_to_coord(corner, rows, cols):
    corners = {
        1: (0, cols - 1),          # top-right
        2: (rows - 1, cols - 1),   # bottom-right
        3: (rows - 1, 0),          # bottom-left
        4: (0, 0),                 # top-left
    }
    return corners.get(corner)

def parse_args():
    parser = argparse.ArgumentParser(description="Micromouse Maze Tool")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--view", type=str, help="Path to map.txt")

    parser.add_argument("--gui", action="store_true",
                        help="Use GUI for generation")

    parser.add_argument("--size", type=parse_pair,
                        help="Maze size rows,cols")

    parser.add_argument("--target-coordinates", type=parse_pair,
                        help="Target cell row,col")

    parser.add_argument("--loops", action="store_true",
                        help="Allow loops")

    parser.add_argument("--set-start", type=int, choices=[1, 2, 3, 4],
                        help="Corner start (1-4)")

    parser.add_argument("--count", type=int, default=1,
                        help="Number of mazes")

    return parser.parse_args()

def  main_generate(gui, config, size, count):

    if gui:
        main_generate_gui(config, size)
    else:
        main_generate_cli(config, size, count)

def main_generate_gui(config, size):
    generator = MazeGeneratorGUI(config)

    rows, cols = size
    maze = Maze(rows, cols, generator)
    maze.generate()

    root = tk.Tk()
    root.title("Maze Generator (GUI)")

    MazeGUI(root, maze)
    root.mainloop()

def main_generate_cli(config, size, count):
    os.makedirs("maze", exist_ok=True)

    rows, cols = size
    for i in range(count):
        generator = MazeGeneratorCLI(config)

        maze = Maze(rows, cols, generator)
        maze.generate()

        folder = save_maze(maze)
        print(f"Saved {folder}/map.txt")

def main_view(raw_path):

    file_path = parse_view_path(raw_path)
    rows, cols, generator = load_maze(file_path)

    maze = Maze(rows, cols, generator)
    maze.generate()

    root = tk.Tk()
    root.title(f"Viewing {file_path}")

    MazeGUI(root, maze)
    root.mainloop()

def parse_view_path(raw_path: str) -> str:

    if ".txt" in raw_path and "/" in raw_path:
        file_path = raw_path 
    elif "/" in raw_path:
        file_path = os.path.join(raw_path, "map.txt")
    else:
        file_path = os.path.join("maze", raw_path, "map.txt")

    return file_path

def main(args):

    if args.generate:
        size = args.size if args.size else (20, 20)

        start = None
        if args.set_start:
            start = corner_to_coord(args.set_start, *size)
        
        config = GeneratorConfig(
            loops=args.loops,
            target=args.target_coordinates,
            start=start
        ) 
        main_generate(args.gui, config, size, args.count)

    elif args.view:
        main_view(args.view)