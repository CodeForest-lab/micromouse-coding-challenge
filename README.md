# MicroMouse Coding Challenge 

This is a coding challenge adaptation of the robotic [Micromouse](https://en.wikipedia.org/wiki/Micromouse) challenge. 

The challenge consists of creating an algorithm to navigate a maze in the fastest time possible. The "mouse" starts in a random corner and needs to navigate to a "room" somewhere in the maze. In this digital adaptation, the clock is represented by game ticks. At every point in the maze the mouse can make a move in at least one direction. Each move costs a game tick and to simmulate that in real life some moves take longer time for a robot to perform, the cost of moves in the game is varying. This means that the shortest route not always means the fastest.
- Going in a straight line costs **1 tick**
- Making a turn costs **3 ticks**
- Going in the opposit direction costs **4 ticks**  

There are two three fazes to the game; **Phase 1**, **Return** phase and **Phase 2**

### Phase 1
This is the blind phase. Here the algorithm is placed in a random corner in a maze it has never seen before. The algorithm needs to explor and find a path to the target room, every move counts. The fewer moves the better. The "clock" stops when the mouse reaches the room. At that moment the **Return** phase starts.


### Return phase 
Now the clock is stopped and all moves are free. Your algorithm is now free to explore the whole maze however when it is done exploring you must return to the start point meaning the corner where you started Phase 1. When the mouse enters the start square **Phase 2** will begin. If the mouse takes "too" long to get back to the start, the game will time out and you will get a zero score for Phase 2.

### Phase 2 
The alorithm now has a second go on the same maze with whatever information you gathered during the Return phase. The clock is reset and the goal is still to get to the target room however this time there is no exploration since you know the location of the room and all paths there.


### Scoring 
Each run consists of running these three phases on a generated maze. This will give each player two scores:
- Total number of ticks in Phase 1 
- Total number of ticks in Phase 2  

## Contents

The code contains three parts: 
- The maze generation 
- The game engine
- The solution algorithm 

An optional visualization tool is available at: 

## How it works 

### Generating the maze
The repo includes a file called `generate_maze.py`. This file can be ran in cli or graphical mode to generate mazes. An example maze is already generated to start with in the reposetory under the `/maze` directory. In there is also a [README.md](./maze/README.md) file containing the information on the maze file format. This knowledge is not needed for contestents.

There are multiple parameters that can be passed to the `generate_maze.py` program including:
- `--size <x>,<y>` for the size of a 
- `--target-coordinates <x>,<y>` to set coordinate of the target room
- `--loops` for allowing loops in the maze
- `--set-start <corner_number>` where the the `corner_number` is  1, 2, 3 or 4 starting from the top right corner and going clockwise.
- `--count <number>` where `number` is the number of mazes to generate
- `--gui` to launch the graphical user interface. (will ignore `--count`)
