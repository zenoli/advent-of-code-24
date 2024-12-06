from typing import Literal


type Grid = list[list[str]]
Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def rot_right(direction):
    x, y = direction
    return y, -x


def rot_left(direction):
    x, y = direction
    return -y, x


def read_input(filename: str):
    with open(filename) as file:
        lines = [list(line.rstrip()) for line in file]
    return lines


def debug(grid: Grid):
    for line in grid:
        print("".join(line))


class StuckInLoopException(Exception):
    pass


def find_walk(start: Position, direction: Direction, grid: Grid) -> set[Position]:
    def next_pos(pos: Position, dir: Direction) -> Position:
        return add(pos, dir)

    def get(pos: Position) -> str:
        return grid[pos[0]][pos[1]]

    def in_bounds(pos: Position) -> bool:
        x_limit = len(grid)
        y_limit = len(grid[0])
        return pos[0] >= 0 and pos[0] < x_limit and pos[1] >= 0 and pos[1] < y_limit

    visited: set[Position] = {start}
    corners: set[tuple[Position, Direction]] = set()

    pos = start
    dir = direction

    while True:
        next = next_pos(pos, dir)
        if (next, dir) in corners:
            raise StuckInLoopException
        if not in_bounds(next):
            break
        symbol = get(next)
        if symbol in ".^":
            visited.add(next)
            pos = next
        elif symbol == "#":
            corners.add((pos, dir))
            dir = rot_right(dir)

    return visited


def find_start(grid) -> Position:
    for x, line in enumerate(grid):
        if (y := "".join(line).find("^")) != -1:
            return (x, y)
    else:
        raise ValueError("Grid does not contain a starting position")


def main():
    # grid = read_input("sample.txt")
    grid = read_input("input.txt")
    start = find_start(grid)
    visited = find_walk(start, UP, grid)

    def set_obstacle(pos: Position):
        grid[pos[0]][pos[1]] = "#"

    def remove_obstacle(pos: Position):
        grid[pos[0]][pos[1]] = "."

    count = 0
    for pos in visited:
        set_obstacle(pos)
        try:
            find_walk(start, UP, grid)
        except StuckInLoopException as e:
            count += 1
        remove_obstacle(pos)
    print(count)


if __name__ == "__main__":
    main()
