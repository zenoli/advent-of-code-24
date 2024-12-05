from itertools import pairwise


def read_input(filename: str) -> list[list[int]]:
    with open(filename) as file:
        lines = [list(map(int, line.split())) for line in file]
    return lines


def diffs(xs: list[int]):
    return [x1 - x2 for x1, x2 in pairwise(xs)]


def is_inc(diffs: list[int]) -> bool:
    return all(map(lambda x: x > 0, diffs))


def is_dec(diffs: list[int]) -> bool:
    return all(map(lambda x: x < 0, diffs))


def is_safe(diffs: list[int]) -> bool:
    return (is_inc(diffs) or is_dec(diffs)) and all(
        map(lambda d: abs(d) in range(1, 4), diffs)
    )


def main():
    # lines = read_input("sample.txt")
    lines = read_input("input.txt")
    result = sum(map(is_safe, map(diffs, lines)))
    print(result)


if __name__ == "__main__":
    main()
