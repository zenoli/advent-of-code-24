from collections.abc import Iterable
from itertools import product, chain

type Grid = list[str]
type Location = tuple[int, int]


def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def get_directions(x: int, y: int) -> Iterable[Iterable[Location]]:
    multipliers = (m for m in product([-1, 0, 1], repeat=2) if m != (0, 0))

    def scale(multiplier: int, start: int) -> Iterable[int]:
        return (o * multiplier + start for o in range(4))

    return (zip(scale(mx, x), scale(my, y)) for mx, my in multipliers)


def extract_word(locations: Iterable[Location], grid: Grid) -> str:
    def get(loc: Location):
        return grid[loc[0]][loc[1]]

    def in_bound(loc: Location) -> bool:
        x_size = len(grid)
        y_size = len(grid[0])
        return loc[0] >= 0 and loc[0] < x_size and loc[1] >= 0 and loc[1] < y_size

    return "".join(get(loc) for loc in locations if in_bound(loc))


def main():
    grid = read_input("sample.txt")
    grid = read_input("input.txt")
    x_size = len(grid)
    y_size = len(grid[0])

    extracted_words = (
        extract_word(locations, grid)
        for locations in chain.from_iterable(
            get_directions(*start) for start in product(range(x_size), range(y_size))
        )
    )
    print(sum(1 for word in extracted_words if word == "XMAS"))


if __name__ == "__main__":
    main()
