import argparse
import os
import tkinter as tk

from maze.maze_core import Maze
from maze.maze_generators import (
    MazeGeneratorCLI,
    MazeGeneratorGUI,
)
from maze.maze_io import save_maze, load_maze
from maze.maze_gui import MazeGUI


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

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


# --------------------------------------------------
# ARGUMENTS
# --------------------------------------------------

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


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    args = parse_args()

    # Defaults
    rows, cols = args.size if args.size else (20, 20)

    start = None
    if args.set_start:
        start = corner_to_coord(args.set_start, rows, cols)

    target = args.target_coordinates

    # --------------------------------------------------
    # GENERATE
    # --------------------------------------------------

    if args.generate:

        # ---------- GUI MODE ----------
        if args.gui:
            config = {
                "loops": args.loops,
                "target": target,
                "start": start,
            }

            generator = MazeGeneratorGUI(config)

            maze = Maze(rows, cols, generator)
            maze.generate()

            root = tk.Tk()
            root.title("Maze Generator (GUI)")

            MazeGUI(root, maze)
            root.mainloop()

        # ---------- CLI MODE ----------
        else:
            os.makedirs("maze", exist_ok=True)

            for i in range(args.count):
                generator = MazeGeneratorCLI(
                    loops=args.loops,
                    target=target,
                    start=start
                )

                maze = Maze(rows, cols, generator)
                maze.generate()

                folder = save_maze(maze)
                print(f"Saved {folder}/map.txt")

    # --------------------------------------------------
    # VIEW
    # --------------------------------------------------

    elif args.view:
        if ".txt" in args.view and "/" in args.view:
            file_path = args.view 
        elif "/" in args.view:
            file_path = os.path.join(args.view, "map.txt")
        else:
            file_path = os.path.join("maze", args.view, "map.txt")

        rows, cols, generator = load_maze(file_path)

        maze = Maze(rows, cols, generator)
        maze.generate()

        root = tk.Tk()
        root.title(f"Viewing {file_path}")

        MazeGUI(root, maze)
        root.mainloop()


# --------------------------------------------------

if __name__ == "__main__":
    main()