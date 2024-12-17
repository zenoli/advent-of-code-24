from itertools import product


type Grid = list[list[str]]
type Position = tuple[int, int]
type Direction = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


directions = {UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3}


def add(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Position, b: Position) -> Position:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename: str) -> tuple[Grid, str]:
    def parse_input(lines: list[str]):
        grid = []
        scanning_grid = True
        instructions = []
        for line in lines:
            if line == "":
                scanning_grid = False
            if scanning_grid:
                grid.append(list(line))
            else:
                instructions.append(line)
        return grid, "".join(instructions)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return parse_input(lines)


def debug(grid):
    for line in grid:
        print("".join(line))


def main():
    def get_val(pos: Position) -> str:
        return grid[pos[0]][pos[1]]

    def set_val(pos: Position, val: str):
        grid[pos[0]][pos[1]] = val

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def find(symbol: str) -> Position:
        for pos in product(range(x_size), range(y_size)):
            if get_val(pos) == symbol:
                return pos
        raise ValueError(f"Symbol {symbol} not found")

    def can_move(pos: Position, dir: Direction) -> bool:
        encountered_obstacle = False
        for symbol in map(get_val, iterate(pos, dir)):
            if symbol == "#":
                encountered_obstacle = True
            if symbol == "." and not encountered_obstacle:
                return True
        return False

    def iterate(pos: Position, dir: Direction):
        next = pos
        while in_bounds(next := add(pos, dir)):
            yield next
            pos = next

    def iterate_block(pos: Position, dir: Direction):
        yield pos
        for next in iterate(pos, dir):
            if get_val(next) not in ".#":
                yield next
            else:
                return

    def try_move(pos: Position, dir: Direction):
        if can_move(pos, dir):
            return move(pos, dir)
        else:
            return pos

    def move(pos, dir):
        block = list(map(get_val, iterate_block(pos, dir)))
        set_val(pos, ".")
        next = add(pos, dir)
        new_pos = next
        for symbol in block:
            set_val(next, symbol)
            next = add(next, dir)
        return new_pos

    def calculate_gps(grid: Grid):
        return sum(
            100 * pos[0] + pos[1]
            for pos in product(range(x_size), range(y_size))
            if get_val(pos) == "O"
        )

    # grid, instructions = read_input("sample.txt")
    grid, instructions = read_input("input.txt")

    instruction_map = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}

    x_size = len(grid)
    y_size = len(grid[0])

    start = find("@")

    pos = start
    for instruction in instructions:
        pos = try_move(pos, instruction_map[instruction])
    debug(grid)
    result = calculate_gps(grid)
    print(result)


if __name__ == "__main__":
    main()
