from itertools import product
from typing import Iterable


type Grid = list[str]
type Position = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def add(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Position, b: Position) -> Position:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename: str) -> Grid:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def debug(grid):
    for line in grid:
        print("".join(line))


def init_grid(val, x_size, y_size):
    return [[val for _ in range(y_size)] for _ in range(x_size)]


def main():
    def get_val(pos: Position) -> str:
        return grid[pos[0]][pos[1]]

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def find(symbol: str) -> Position:
        for pos in product(range(x_size), range(y_size)):
            if get_val(pos) == symbol:
                return pos
        raise ValueError(f"Symbol {symbol} not found")

    def get_neighbors(pos: Position) -> Iterable[Position]:
        return (
            add(pos, dir) for dir in DIRECTIONS if in_bounds(neighbor := add(pos, dir))
        )

    def race(start, end):
        def get_next(pos: Position) -> Position:
            for neighbor in get_neighbors(pos):
                if get_val(neighbor) != "#" and neighbor not in steps:
                    return neighbor

        steps = {}
        count = 0

        steps[start] = 0
        pos = start
        while pos != end:
            steps[pos] = (count := count + 1)
            pos = get_next(pos)
        print(steps)

    grid = read_input("sample.txt")
    x_size = len(grid)
    y_size = len(grid[0])

    debug(grid)
    start = find("S")
    end = find("E")

    race(start, end)


if __name__ == "__main__":
    main()
