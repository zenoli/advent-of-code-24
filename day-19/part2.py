from functools import cache


def read_input(filename: str):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    patterns = [pattern.strip() for pattern in lines[0].split(",")]
    designs = lines[2:]
    return tuple(patterns), designs


def debug(grid):
    for line in grid:
        print("".join(line))


def init_grid(val, x_size, y_size):
    return [[val for _ in range(y_size)] for _ in range(x_size)]


@cache
def count_designs(patterns: tuple[str], design: str) -> int:
    if design == "":
        return 1
    return sum(
        count_designs(patterns, design[len(pattern) :])
        for pattern in patterns
        if design.startswith(pattern)
    )


def main():
    # patterns, designs = read_input("sample.txt")
    patterns, designs = read_input("input.txt")
    print(sum(count_designs(patterns, design) for design in designs))


if __name__ == "__main__":
    main()
