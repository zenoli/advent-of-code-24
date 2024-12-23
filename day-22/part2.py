from collections import defaultdict
from itertools import pairwise

type Seq = tuple[int, int, int, int]


def read_input(filename: str) -> list[int]:
    with open(filename) as file:
        lines = [int(line.rstrip()) for line in file]
    return lines  # pyright: ignore


def evolve(s: int) -> int:
    s = ((s << 6) ^ s) % (1 << 24)
    s = ((s >> 5) ^ s) % (1 << 24)
    s = ((s << 11) ^ s) % (1 << 24)
    return s


def get_prices(init_s: int):
    s = init_s
    prices = [init_s % 10]
    for _ in range(2000):
        s = evolve(s)
        prices.append(s % 10)
    return prices


def get_changes(prices: list[int]):
    return list(zip((y - x for x, y in pairwise(prices)), prices[1:]))


def get_sequences(changes: list[tuple[int, int]]):
    for i in range(3, len(changes)):
        seq = (
            changes[i - 3][0],
            changes[i - 2][0],
            changes[i - 1][0],
            changes[i - 0][0],
        )
        yield (seq, changes[i][1])


def main():
    # secrets = read_input("sample-part2.txt")
    secrets = read_input("input.txt")

    solutions: dict[Seq, dict] = defaultdict(dict)
    for init_s in secrets:
        prices = get_prices(init_s)
        changes = get_changes(prices)
        sequences = get_sequences(changes)
        for seq, price in sequences:
            if init_s not in solutions[seq]:
                solutions[seq][init_s] = price

    max_solution = 0
    for seq, solution in solutions.items():
        max_solution = max(max_solution, sum(solution.values()))

    print(max_solution)


if __name__ == "__main__":
    main()
