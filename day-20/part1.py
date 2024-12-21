from collections import Counter
from itertools import product, chain
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

    def compute_time_saved(pos: Position, times: dict[Position, int]):
        for dir in DIRECTIONS:
            next1 = add(pos, dir)
            if not in_bounds(next1) or get_val(next1) != "#":
                continue
            next2 = add(next1, dir)
            if not in_bounds(next2) or get_val(next2) == "#":
                continue
            next = next2
            if next in times:
                time_saved = times[next] - (times[pos] + 2)
                if time_saved > 0:
                    yield time_saved

    # grid = read_input("sample.txt")
    grid = read_input("input.txt")
    x_size = len(grid)
    y_size = len(grid[0])

    start = find("S")
    end = find("E")

    times = race(start, end)
    cheats = chain.from_iterable(compute_time_saved(pos, times) for pos in times)
    result = sum(time_saved >= 100 for time_saved in cheats)
    print(result)


if __name__ == "__main__":
    main()
