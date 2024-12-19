def read_input(filename: str):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    patterns = [pattern.strip() for pattern in lines[0].split(",")]
    designs = lines[2:]
    return patterns, designs


def debug(grid):
    for line in grid:
        print("".join(line))


def init_grid(val, x_size, y_size):
    return [[val for _ in range(y_size)] for _ in range(x_size)]


def can_design(patterns: list[str], design: str) -> bool:
    if design == "":
        return True
    return any(
        can_design(patterns, design[len(pattern) :])
        for pattern in patterns
        if design.startswith(pattern)
    )


def main():
    # patterns, designs = read_input("sample.txt")
    patterns, designs = read_input("input.txt")
    print(sum(can_design(patterns, design) for design in designs))


if __name__ == "__main__":
    main()
