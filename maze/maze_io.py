import os
import re

from maze.maze_generators import MazeGeneratorFromFile


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def _maze_to_ascii(maze):
    lines = []

    for r in range(maze.rows):
        row_chars = []

        for c in range(maze.cols):
            cell = maze.get_cell(r, c)

            value = 0x40

            # bit0 = north
            if cell.walls["top"]:
                value |= 1 << 0

            # bit1 = east
            if cell.walls["right"]:
                value |= 1 << 1

            # bit2 = south
            if cell.walls["bottom"]:
                value |= 1 << 2

            # bit3 = west
            if cell.walls["left"]:
                value |= 1 << 3

            # bit5 = target
            if cell.is_target:
                value |= 1 << 5

            row_chars.append(chr(value))

        lines.append("".join(row_chars))

    return lines


def save_maze(maze, base_dir="maze"):
    index = get_index(base_dir)
    folder_name = f"maze_{index}"
    folder_path = os.path.join(base_dir, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "map.txt")
    
    with open(file_path, "w") as f:
        for line in _maze_to_ascii(maze):
            f.write(line + "\n")

    return folder_path

def get_index(base_dir):
    pattern = re.compile(r"maze_(\d+)")
    existing_indices = []

    os.makedirs(base_dir, exist_ok=True)

    for name in os.listdir(base_dir):
        match = pattern.fullmatch(name)
        if match and os.path.isdir(os.path.join(base_dir, name)):
            existing_indices.append(int(match.group(1)))

    if existing_indices:
        next_index = max(existing_indices) + 1
    else:
        next_index = 1

    return next_index

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_maze(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    rows = len(lines)
    cols = len(lines[0])

    grid_data = []

    for r in range(rows):
        row = []

        for c in range(cols):
            value = ord(lines[r][c])

            walls = {
                "top": bool(value & (1 << 0)),
                "right": bool(value & (1 << 1)),
                "bottom": bool(value & (1 << 2)),
                "left": bool(value & (1 << 3)),
            }

            is_target = bool(value & (1 << 5))

            row.append({
                "walls": walls,
                "target": is_target
            })

        grid_data.append(row)

    generator = MazeGeneratorFromFile(grid_data)

    return rows, cols, generator