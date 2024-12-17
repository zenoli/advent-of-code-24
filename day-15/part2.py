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


def read_input(filename: str, duplicate=True) -> tuple[Grid, str]:
    def duplicate_line(line: str):
        result = ""
        for c in line:
            if c in ".#":
                result += c * 2
            if c == "@":
                result += "@."
            if c == "O":
                result += "[]"
        return list(result)

    def parse_input(lines: list[str]):
        grid: Grid = []
        scanning_grid = True
        instructions = []
        for line in lines:
            if line == "":
                scanning_grid = False
            if scanning_grid:
                grid.append(duplicate_line(line) if duplicate else list(line))
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

    def can_move_horizontal(pos: Position, dir: Direction) -> bool:
        assert dir in {LEFT, RIGHT}
        symbol = get_val(pos)
        if symbol == ".":
            return True
        if symbol == "#":
            return False
        return can_move_horizontal(add(pos, dir), dir)

    def move_horizontal(pos: Position, dir: Direction):
        assert dir in {LEFT, RIGHT}
        symbol = get_val(pos)
        if symbol == ".":
            return
        move_horizontal(add(pos, dir), dir)
        set_val(pos, ".")
        set_val(add(pos, dir), symbol)

    def try_move_horizontal(pos: Position, dir: Direction):
        if can_move_horizontal(pos, dir):
            move_horizontal(pos, dir)
            return True
        return False

    def can_move_vertical(pos: Position, dir: Direction) -> bool:
        assert dir in {UP, DOWN}
        symbol = get_val(pos)
        if symbol == ".":
            return True
        if symbol == "#":
            return False
        next_positions = {add(pos, dir)}
        if symbol == "[":
            other_pos = add(pos, RIGHT)
            next_positions.add(add(other_pos, dir))
        if symbol == "]":
            other_pos = add(pos, LEFT)
            next_positions.add(add(other_pos, dir))

        if all(get_val(next) == "." for next in next_positions):
            return True

        return all(can_move_vertical(next, dir) for next in next_positions)

    def move_vertical(pos: Position, dir: Direction):
        assert dir in {UP, DOWN}
        symbol = get_val(pos)
        if symbol == ".":
            return

        next_positions = {add(pos, dir)}
        if symbol == "[":
            other_pos = add(pos, RIGHT)
            next_positions.add(add(other_pos, dir))
        if symbol == "]":
            other_pos = add(pos, LEFT)
            next_positions.add(add(other_pos, dir))
        for next in next_positions:
            move_vertical(next, dir)

        if symbol == "@":
            set_val(pos, ".")
            set_val(add(pos, dir), "@")
        if symbol == "[":
            other_pos = add(pos, RIGHT)
            set_val(pos, ".")
            set_val(other_pos, ".")
            set_val(add(pos, dir), "[")
            set_val(add(other_pos, dir), "]")
        if symbol == "]":
            other_pos = add(pos, LEFT)
            set_val(pos, ".")
            set_val(other_pos, ".")
            set_val(add(pos, dir), "]")
            set_val(add(other_pos, dir), "[")

    def try_move_vertical(pos: Position, dir: Direction):
        if can_move_vertical(pos, dir):
            move_vertical(pos, dir)
            return True
        return False

    def try_move(pos: Position, dir: Direction):
        if dir in {UP, DOWN}:
            return try_move_vertical(pos, dir)
        else:
            return try_move_horizontal(pos, dir)

    def calculate_gps(grid: Grid):
        return sum(
            100 * pos[0] + pos[1]
            for pos in product(range(x_size), range(y_size))
            if get_val(pos) == "["
        )

    # grid, instructions = read_input("sample-part2.txt")
    # grid, instructions = read_input("debug.txt", duplicate=False)
    grid, instructions = read_input("input.txt")

    instruction_map = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT}

    x_size = len(grid)
    y_size = len(grid[0])

    start = find("@")

    debug(grid)
    print("")
    pos = start
    for instruction in instructions:
        dir = instruction_map[instruction]
        if try_move(pos, dir):
            pos = add(pos, dir)
        print("")

    result = calculate_gps(grid)
    print(result)


if __name__ == "__main__":
    main()
