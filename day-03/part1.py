# Aoc 24 - Day 3, Part 1
import re
from ast import literal_eval


def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line for line in file]
    return lines


def solve(line):
    matches = re.findall(r"(?<=mul)\(\d+,\d+\)", line)
    result = sum(x * y for x, y in map(literal_eval, matches))
    return result


def main():
    # lines = read_input("sample.txt")
    lines = read_input("input.txt")
    result = sum(map(solve, lines))

    print(result)


if __name__ == "__main__":
    main()
