from itertools import pairwise


def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def neighbors(i: int, j: int, grid: list[str]):
    def _neighbors():
        yield i - 1, j - 1
        yield i - 1, j
        yield i - 1, j + 1

        yield i, j - 1
        yield i, j + 1

        yield i + 1, j - 1
        yield i + 1, j
        yield i + 1, j + 1

    i_max = len(grid)
    j_max = len(grid[0])

    return (
        (i_p, j_p)
        for i_p, j_p in _neighbors()
        if i_p >= 0 and j_p >= 0 and i_p < i_max and j_p < j_max
    )


def count_s(i: int, j: int, grid: list[str]) -> int:
    return 1 if grid[i][j] == "S" else 0


def count_as(i: int, j: int, grid: list[str]) -> int:
    count = 0

    if grid[i][j] != "A":
        return count
    return sum(count_s(i_p, j_p, grid) for i_p, j_p in neighbors(i, j, grid))


def count_mas(i: int, j: int, grid: list[str]) -> int:
    count = 0

    if grid[i][j] != "M":
        return count
    return sum(count_as(i_p, j_p, grid) for i_p, j_p in neighbors(i, j, grid))


def count_xmas(i: int, j: int, grid: list[str]) -> int:
    count = 0

    if grid[i][j] != "X":
        return count
    return sum(count_mas(i_p, j_p, grid) for i_p, j_p in neighbors(i, j, grid))


def main():
    grid = read_input("sample-part1.txt")
    # lines = read_input("input.txt")
    for line in grid:
        print(line)

    i_max = len(grid)
    j_max = len(grid[0])

    print(count_xmas(0, 4, grid))

    count = 0

    for i in range(i_max):
        for j in range(j_max):
            count += count_xmas(i, j, grid)

    print(count)

    # for i, j in neighbors(i_max, 1, grid):
    #     print(i, j)
    # print(lines)


if __name__ == "__main__":
    main()
