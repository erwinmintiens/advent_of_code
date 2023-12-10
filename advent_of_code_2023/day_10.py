"""--- Day 10: Pipe Maze ---

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....

In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF

In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....

You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....

In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...

Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...

Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

ANSWER: 6931
"""


class Coordinates:
    def __init__(self, x: int, y: int, value: str | None = None) -> None:
        self.x = x
        self.y = y
        self.value = value

    def set_value(self, maze) -> None:
        self.value = maze.get_position_value(self)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Maze:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.starting_position: Coordinates = self.get_starting_position()
        self.current_position = self.starting_position
        self.previous_position = Coordinates(0, 0)

    def get_starting_position(self) -> Coordinates:
        for y_index, line in enumerate(self.lines):
            if "S" in line:
                return Coordinates(line.index("S"), y_index, "S")
        else:
            return Coordinates(0, 0)

    def get_position_value(self, coordinates: Coordinates) -> str:
        return self.lines[coordinates.y][coordinates.x]

    def go_down(self):
        self.previous_position = self.current_position
        self.current_position = Coordinates(
            self.current_position.x, self.current_position.y + 1
        )
        self.current_position.value = self.get_position_value(self.current_position)

    def go_right(self):
        self.previous_position = self.current_position
        self.current_position = Coordinates(
            self.current_position.x + 1, self.current_position.y
        )
        self.current_position.value = self.get_position_value(self.current_position)

    def go_up(self):
        self.previous_position = self.current_position
        self.current_position = Coordinates(
            self.current_position.x, self.current_position.y - 1
        )
        self.current_position.value = self.get_position_value(self.current_position)

    def go_left(self):
        self.previous_position = self.current_position
        self.current_position = Coordinates(
            self.current_position.x - 1, self.current_position.y
        )
        self.current_position.value = self.get_position_value(self.current_position)

    def coming_from_left(self) -> bool:
        return self.current_position.x > self.previous_position.x

    def coming_from_above(self) -> bool:
        return self.current_position.y > self.previous_position.y

    def coming_from_right(self) -> bool:
        return self.current_position.x < self.previous_position.x

    def coming_from_below(self) -> bool:
        return self.current_position.y < self.previous_position.y

    def next_position(self):
        match self.current_position.value:
            case "S":
                return self.get_starting_direction()
            case "F":
                self.go_down() if self.coming_from_right() else self.go_right()
            case "J":
                self.go_up() if self.coming_from_left() else self.go_left()
            case "7":
                self.go_down() if self.coming_from_left() else self.go_left()
            case "L":
                self.go_up() if self.coming_from_right() else self.go_right()
            case "-":
                self.go_right() if self.coming_from_left() else self.go_left()
            case "|":
                self.go_down() if self.coming_from_above() else self.go_up()

    def get_starting_direction(self):
        for coordinates_shift in [
            (0, 1, ["|", "J", "L"]),
            (1, 0, ["-", "J", "7"]),
            (-1, 0, ["-", "F", "L"]),
            (0, -1, "|", "F", "7"),
        ]:
            coordinates = Coordinates(
                self.starting_position.x + coordinates_shift[0],
                self.starting_position.y + coordinates_shift[1],
            )
            coordinates.set_value(self)
            if coordinates.value in coordinates_shift[2]:
                self.previous_position = self.starting_position
                self.current_position = coordinates


def read_input(file_name: str) -> list[str]:
    with open(file_name, "r") as myfile:
        lines = [line.strip() for line in myfile]
    return lines


def part1():
    lines = read_input("input_files/input_day_10.txt")
    maze = Maze(lines)
    maze.next_position()
    number_of_steps = 1
    while maze.current_position != maze.starting_position:
        maze.next_position()
        number_of_steps += 1
    print(f"Number of steps: {int(number_of_steps / 2)}")


if __name__ == "__main__":
    part1()
