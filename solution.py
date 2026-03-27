import random

"""
This is the solution class where you can add any methods or member variables you want but 
don't change the name of the class or the method get_step().
However change the value of teamname to what you want your team to be called.
"""
class Solution:
    teamname = "test_team"

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
    dictionary is True is invalud.  
    """
    def get_step(self, cell: dict):
        
        # Simple test example, check which directions do not have a wall and then pick one 
        # those directions randomly
        avail_directions = []
        for direction in cell["walls"]:
            if not cell["walls"][direction]:
                avail_directions.append(direction)

        return random.choice(avail_directions) 