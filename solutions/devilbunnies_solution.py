import random
import math 

"""
This is the solution class where you can add any methods or member variables you want but 
don't change the name of the class or the method get_step().
However change the value of teamname to what you want your team to be called.
"""

class Solution:
    teamname = "DevilBunnies"

    def __init__(self):
        self.phase = 0
        self.position = (0, 0)
        self.start = (0, 0)
        self.visited = set()
        self.target = None
        self.to_explore = []
        self.maximum = (0, 0)

    PHASES = ['phase1', 'return', 'phase2']
    DIRECTIONS = ['top', 'right', 'bottom', 'left']
    MOVEMENT = {
        "top": (-1, 0),
        "right": (0, 1),
        "bottom": (1, 0),
        "left": (0, -1)
    }

    OPPOSIT = {
        "top": "bottom",
        "right": "left",
        "bottom": "top",
        "left": "right"
    } 

    """ The api into your solution by the 'game engien'. The function get_step() method
    takes information regarding the current cell and returns in which direction to walk next.
    Allowed directions are:
        ["top", "right", "bottom", "left"]

    The cell parameter is a dictionary and contain two keys:
        "walls": {
            "top": bool,
            "right": bool,
            "bottom": bool,
            "left": bool 
        }
        "target": bool -> true if you are at the target location 

    The boolean value for the walls represents if there is a wall in that direction at the 
    current cell. This means trying to take a step in a direction where the value walls 
    dictionary is True is an invalid move and will cause the run to crash.  
    """
    def get_step(self, cell: dict):
        self.visited.add(self.position)
        self.update_maximum(self.position)

        match self.PHASES[self.phase]:
            case "phase1":
                return self.phase_1(cell)
            case "return":
                return self.phase_return(cell)
            case "phase2":
                return self.phase_2(cell)

        return "stop" 

    def phase_1(self, cell):
        if cell["target"]:
            self.phase+=1
        
        mod = lambda a : a
        weighted = self.get_weighted_directions(cell, mod)
        return self.get_next_direction(cell, weighted)

    def phase_return(self, cell):
        if self.position == self.start:
            self.phase+=1
            self.visited = set(self.position)

        mod = lambda a : a/2
        weighted = self.get_weighted_directions(cell, mod)
        return self.get_next_direction(cell, weighted)
    
    def phase_2(self, cell):
        mod = lambda a : a/2
        weighted = self.get_weighted_directions(cell, mod)
        return self.get_next_direction(cell, weighted)
 
    def get_next_direction(self, cell, weighted):
        for dir_set in weighted:
            self.to_explore.append(self.OPPOSIT[dir_set[1]])
            self.position = dir_set[2]
            return dir_set[1]

        if self.to_explore:
            direction = self.to_explore.pop()
            self.position = self.move_direction(self.position, direction)
            return direction
        
        return "stop"

    def move_direction(self, pos, direction):
        p_r, p_c = pos
        move_r, move_c = self.MOVEMENT[direction]
        return (p_r + move_r, p_c + move_c)
    
    def update_maximum(self, pos):
        if abs(pos[0]) > abs(self.maximum[0]):
            self.maximum = (pos[0], self.maximum[1])
        elif abs(pos[1]) > abs(self.maximum[1]):
            self.maximum = (self.maximum[0], pos[1])


    def get_weighted_directions(self, cell, mod):
        weighted = []
        for direction in self.DIRECTIONS:
            if not cell["walls"][direction]:
                next_pos = self.move_direction(self.position, direction)   

                if next_pos not in self.visited:
                    weighted.append((self.geo_distance(next_pos, mod), direction, next_pos))

        return sorted(weighted, key=lambda a : a[0])

    def geo_distance(self, pos, max_mod=None):
        if not max_mod:
            max_mod = lambda a : a
        t_r, t_c = max_mod(self.maximum[0]), max_mod(self.maximum[1])
        return math.sqrt((t_r - pos[0])**2 + (t_c - pos[1])**2)
    
