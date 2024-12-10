from itertools import product


type Grid = list[str]
type Position = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


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

    def get(pos: Position) -> int:
        return int(grid[pos[0]][pos[1]])

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def score(pos: Position) -> set[Position]:
        if not in_bounds(pos):
            return set()
        val = get(pos)

        result = set()
        if val == 9:
            return {pos}

        for dir in [UP, DOWN, LEFT, RIGHT]:
            next = add(pos, dir)
            if in_bounds(next) and get(next) == val + 1:
                result = result | score(next)

        return result

    result = sum(
        len(score(pos))
        for pos in product(range(x_size), range(y_size))
        if get(pos) == 0
    )

    print(result)


if __name__ == "__main__":
    main()
