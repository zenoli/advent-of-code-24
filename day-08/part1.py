from collections import defaultdict
from collections.abc import Mapping
from itertools import combinations, product

type Grid = list[str]
type Location = tuple[int, int]


def add(a: Location, b: Location) -> Location:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Location, b: Location) -> Location:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename: str) -> Grid:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(lines)


def debug(grid: Grid):
    for line in grid:
        print(line)


def get_locations(grid: Grid) -> Mapping[str, list[Location]]:
    def get(pos: Location) -> str:
        return grid[pos[0]][pos[1]]

    x_size = len(grid)
    y_size = len(grid[0])

    locations = defaultdict(list)
    for loc in product(range(x_size), range(y_size)):
        antenna = get(loc)
        if antenna != ".":
            locations[antenna].append(loc)

    return locations


def get_antinodes(a1: Location, a2: Location, grid: Grid) -> list[Location]:
    delta = sub(a2, a1)
    return [sub(a1, delta), add(a2, delta)]


def main():
    # grid = read_input("sample.txt")
    grid = read_input("input.txt")
    x_size = len(grid)
    y_size = len(grid[0])

    # debug(grid)
    locations = get_locations(grid)

    antinodes: set[Location] = set()

    def in_bound(loc: Location):
        return 0 <= loc[0] < x_size and 0 <= loc[1] < y_size

    for _, locs in locations.items():
        for a1, a2 in combinations(locs, 2):
            antinodes.update(get_antinodes(a1, a2, grid))

    result = sum(in_bound(loc) for loc in antinodes)

    print(result)


if __name__ == "__main__":
    main()
