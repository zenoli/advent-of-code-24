from itertools import pairwise


def read_input(filename: str) -> list[list[int]]:
    with open(filename) as file:
        lines = [list(map(int, line.split())) for line in file]
    return lines


def get_diffs(xs: list[int]):
    return [x1 - x2 for x1, x2 in pairwise(xs)]


def is_inc(diffs: list[int]) -> bool:
    return all(map(lambda x: x > 0, diffs))


def is_dec(diffs: list[int]) -> bool:
    return all(map(lambda x: x < 0, diffs))


def is_safe(xs: list[int]) -> bool:
    diffs = get_diffs(xs)
    return (is_inc(diffs) or is_dec(diffs)) and all(
        map(lambda d: abs(d) in range(1, 4), diffs)
    )


def solve(xs: list[int]) -> bool:
    c1 = any(is_safe(xs[:i] + xs[(i + 1) :]) for i in range(len(xs)))
    return c1 or is_safe(xs)


def main():
    # lines = read_input("sample.txt")
    lines = read_input("input.txt")
    result = sum(map(solve, lines))
    print(result)


if __name__ == "__main__":
    main()
