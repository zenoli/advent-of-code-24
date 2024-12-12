from collections.abc import Iterable
from itertools import chain, product
from typing import Counter


type Grid = list[str]
type DoubleGrid = list[list[str]]
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
    return list(lines)


def debug(grid: Grid | DoubleGrid):
    for line in grid:
        print(line)


def get_double_grid(grid: Grid) -> Grid:
    def get_double_line(line: str) -> str:
        return "".join(["#", *((c + c) for c in line), "#"])

    def get_padding_line():
        return "#" * (x_size * 2 + 2)

    x_size = len(grid)
    return [
        get_padding_line(),
        *chain.from_iterable(
            [get_double_line(line), get_double_line(line)] for line in grid
        ),
        get_padding_line(),
    ]


def main():
    def find_corners():
        for x, y in product(range(x_size_double - 1), range(y_size_double - 1)):
            top_left = double_grid[x][y]
            top_right = double_grid[x][y + 1]
            bot_left = double_grid[x + 1][y]
            bot_right = double_grid[x + 1][y + 1]

            counts = Counter(top_left + top_right + bot_left + bot_right)
            if len(counts) == 1:
                # AA
                # AA
                continue
            elif len(counts) == 2:
                if set(counts.values()) == {2, 2}:
                    if top_left == top_right or top_left == bot_left:
                        # AA AB
                        # BB AB
                        continue
                    else:
                        # AB
                        # BA
                        corners[x][y] = True
                        corners[x][y + 1] = True
                        corners[x + 1][y] = True
                        corners[x + 1][y + 1] = True
                elif set(counts.values()) == {1, 3}:
                    if counts[top_left] == 1:
                        # AB
                        # BB
                        corners[x][y] = True
                        corners[x + 1][y + 1] = True
                    elif counts[top_right] == 1:
                        # BA
                        # BB
                        corners[x][y + 1] = True
                        corners[x + 1][y] = True
                    elif counts[bot_left] == 1:
                        # BB
                        # AB
                        corners[x + 1][y] = True
                        corners[x][y + 1] = True
                    else:  # counts[bot_right] == 1
                        # BB
                        # BA
                        corners[x + 1][y + 1] = True
                        corners[x][y] = True

            elif len(counts) == 3:
                if counts[top_left] == 1:
                    corners[x][y] = True
                if counts[top_right] == 1:
                    corners[x][y + 1] = True
                if counts[bot_left] == 1:
                    corners[x + 1][y] = True
                if counts[bot_right] == 1:
                    corners[x + 1][y + 1] = True
            else:  # len(counts) == 4:
                # AB
                # CD
                corners[x][y] = True
                corners[x][y + 1] = True
                corners[x + 1][y] = True
                corners[x + 1][y + 1] = True

    def debug_corners():
        for line in corners:
            print("".join(["o" if c else "." for c in line]))

    grid = read_input("sample.txt")
    double_grid = get_double_grid(grid)
    # grid = read_input("input.txt")

    x_size = len(grid)
    y_size = len(grid[0])

    x_size_double = len(double_grid)
    y_size_double = len(double_grid[0])

    corners = [[False] * y_size_double for _ in range(x_size_double)]

    debug(grid)
    print("")
    debug(double_grid)

    find_corners()

    print("")
    debug_corners()


if __name__ == "__main__":
    main()
