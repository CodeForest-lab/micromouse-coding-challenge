# Maze file format

The maze map file format is very simple. Each position on the maze will be assigned a ASCII character. Which character is used is based on the binary representation of that character. We then assign if there is a wall pressent in each direction to a specific bit. 1 means there is a wall there and 0 means no wall. The directions are like this:

- `bit0` = north
- `bit1` = east
- `bit2` = south
- `bit3` = west

So for example `A` has binary representation `b0100_0001` which means there is a wall to the north but no walls to the east, south or west. `G`on the other hand has binary representation `b0100_0111` which means that the only direction the mouse could walk is west because there are walls to the north, east and south. 

`Bit5` is used to indicate if the position is the target. From the table bellow you can see that setting this bit to 1 is equivelent to setting the character as lower case.

The file format will have equal numer of rows as the number of rows in the maze and each row in the file will have a string that has the same number of characters as the number of columns in the maze.

### Example
If we have a 5x5 maze with the target in the center position it could look like this in the file

```
KIECK
LFIFJ
MCjIB
IBLBN
NLEDW
```

## ASCII Table
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flinuxhandbook.com%2Fcontent%2Fimages%2Fsize%2Fw1000%2F2023%2F01%2F2.png" alt="ASCII characters" width="600">
