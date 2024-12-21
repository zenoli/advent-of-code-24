from collections import Counter
from itertools import product, combinations
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
        return (neighbor for dir in DIRECTIONS if in_bounds(neighbor := add(pos, dir)))

    def race(start, end):
        def get_next(pos: Position):
            for neighbor in get_neighbors(pos):
                if get_val(neighbor) != "#" and neighbor not in times:
                    return neighbor
            raise ValueError(f"No next position found from {pos}.")

        times = {}
        count = 0

        times[start] = 0
        pos = start
        while pos != end:
            times[pos] = count
            count += 1
            pos = get_next(pos)
        times[pos] = count
        return times

    def manhattan_distance(cheat_start: Position, cheat_end: Position) -> int:
        xs, ys = cheat_start
        xe, ye = cheat_end
        return abs(xe - xs) + abs(ye - ys)

    # grid, thresh = read_input("sample.txt"), 50
    grid, thresh = read_input("input.txt"), 100
    x_size = len(grid)
    y_size = len(grid[0])

    start = find("S")
    end = find("E")

    times = race(start, end)
    result = 0
    for cheat_start, cheat_end in combinations(times, 2):
        if (dist := manhattan_distance(cheat_start, cheat_end)) <= 20:
            time_saved = times[cheat_end] - (times[cheat_start] + dist)
            if time_saved >= thresh:
                result += 1

    print(result)


if __name__ == "__main__":
    main()
