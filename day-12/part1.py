from collections.abc import Iterable
from itertools import product


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
    return list(lines)


def debug(grid: Grid):
    for line in grid:
        print(line)


def main():
    # grid = read_input("sample.txt")
    grid = read_input("input.txt")
    debug(grid)

    x_size = len(grid)
    y_size = len(grid[0])
    visited = [[False] * y_size for _ in range(x_size)]

    def get(pos: Position) -> str:
        if not in_bounds(pos):
            return "#"
        else:
            return grid[pos[0]][pos[1]]

    def is_visited(pos: Position) -> int:
        return visited[pos[0]][pos[1]]

    def visit(pos):
        visited[pos[0]][pos[1]] = True

    def get_neighbors(pos: Position) -> Iterable[Position]:
        return (add(pos, dir) for dir in DIRECTIONS)

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def price(start: Position) -> int:
        next_positions = {start}

        area = 0
        diameter = 0

        while len(next_positions) > 0:
            pos = next_positions.pop()
            symbol = get(pos)
            if not is_visited(pos):
                visit(pos)
                area += 1
                for neighbor in get_neighbors(pos):
                    if get(neighbor) != symbol:
                        diameter += 1
                    else:
                        if not is_visited(neighbor):
                            next_positions.add(neighbor)
        return area * diameter

    result = sum(
        price(pos)
        for pos in product(range(x_size), range(y_size))
        if not is_visited(pos)
    )

    print(result)


if __name__ == "__main__":
    main()
