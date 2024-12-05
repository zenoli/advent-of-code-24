from itertools import product

type Grid = list[str]
type Location = tuple[int, int]


def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def check(x, y, grid: Grid) -> bool:
    s1 = {grid[x - 1][y - 1], grid[x + 1][y + 1]}
    s2 = {grid[x + 1][y - 1], grid[x - 1][y + 1]}
    ms = {"M", "S"}
    return s1 == ms and s2 == ms and grid[x][y] == "A"


def main():
    # grid = read_input("sample.txt")
    grid = read_input("input.txt")
    x_size = len(grid)
    y_size = len(grid[0])

    count = sum(
        check(x, y, grid)
        for x, y in product(range(1, x_size - 1), range(1, y_size - 1))
    )

    print(count)


if __name__ == "__main__":
    main()
