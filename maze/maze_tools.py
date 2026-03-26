from collections import deque
import heapq

MAX_GEN_ATTEMPTS = 50

DIRECTIONS = ["top", "right", "bottom", "left"]

# Movement vectors
DIR_VECTORS = {
    "top": (-1, 0),
    "right": (0, 1),
    "bottom": (1, 0),
    "left": (0, -1),
}

# Opposites
OPPOSITE = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left"
}

def shortest_path(maze):
    start = maze.start
    targets = set(maze.get_targets())

    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        r, c = queue.popleft()

        if (r, c) in targets:
            return reconstruct_path(parent, start, (r, c))

        cell = maze.get_cell(r, c)

        for d in DIRECTIONS:
            if not cell.walls[d]:
                dr, dc = DIR_VECTORS[d]
                nr, nc = r + dr, c + dc

                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    queue.append((nr, nc))

    return []


def fastest_path(maze):
    start = maze.start
    targets = set(maze.get_targets())

    heap = []
    heapq.heappush(heap, (0, start[0], start[1], None))

    # Best known cost per state
    best_cost = {}
    parent = {}

    while heap:
        cost, r, c, prev_dir = heapq.heappop(heap)

        state = (r, c, prev_dir)

        # Skip worse states
        if state in best_cost and best_cost[state] <= cost:
            continue

        best_cost[state] = cost

        if (r, c) in targets:
            return reconstruct_path_with_dir(parent, start, (r, c), prev_dir)

        cell = maze.get_cell(r, c)

        for d in DIRECTIONS:
            if cell.walls[d]:
                continue

            dr, dc = DIR_VECTORS[d]
            nr, nc = r + dr, c + dc

            new_cost = cost + compute_cost(prev_dir, d)
            new_state = (nr, nc, d)

            # 🔥 KEY FIX: prune BEFORE pushing
            if new_state in best_cost and best_cost[new_state] <= new_cost:
                continue

            heapq.heappush(heap, (new_cost, nr, nc, d))
            parent[new_state] = (r, c, prev_dir)

    return []


def compute_cost(prev_dir, new_dir):
    if prev_dir is None:
        return 1  # first move

    if prev_dir == new_dir:
        return 1  # straight

    if OPPOSITE[prev_dir] == new_dir:
        return 4  # reverse

    return 3  # turn

def reconstruct_path(parent, start, end):
    path = []
    node = end

    while node != start:
        path.append(node)
        node = parent[node]

    path.append(start)
    return list(reversed(path))

def reconstruct_path_with_dir(parent, start, end, final_dir):
    path = []
    node = (end[0], end[1], final_dir)

    while True:
        r, c, d = node
        path.append((r, c))

        if (r, c) == start:
            break

        node = parent[node]

    return list(reversed(path))

def path_cost(path):
    cost = 0
    prev_dir = None

    for i in range(1, len(path)):
        r1, c1 = path[i - 1]
        r2, c2 = path[i]

        dr = r2 - r1
        dc = c2 - c1

        if dr == -1:
            d = "top"
        elif dr == 1:
            d = "bottom"
        elif dc == -1:
            d = "left"
        else:
            d = "right"

        cost += compute_cost(prev_dir, d)
        prev_dir = d

    return cost

def is_interesting_maze(maze):

    sp = shortest_path(maze)
    fp = fastest_path(maze)

    if not sp or not fp:
        return False

    sp_cost = path_cost(sp)
    fp_cost = path_cost(fp)

    return fp_cost < sp_cost

def generate_until_interesting(maze):
    for _ in range(MAX_GEN_ATTEMPTS):
        maze.generate()

        if is_interesting_maze(maze):
            return True
    else:
        print("Warning: could not generate interesting maze")
        return False