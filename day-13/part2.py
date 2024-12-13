import re
from itertools import batched


def read_input(filename: str):
    def parse_line(line: str) -> tuple[int, ...]:
        return tuple(map(int, re.findall(r"\d+", line)))

    with open(filename) as file:
        lines = [ln for line in file if (ln := line.rstrip()) != ""]

    for btn_line1, btn_line2, price_line in batched(lines, 3):
        x1, y1 = parse_line(btn_line1)
        x2, y2 = parse_line(btn_line2)
        X, Y = parse_line(price_line)
        yield x1, y1, x2, y2, X, Y


def solve(x1, y1, x2, y2, X, Y):
    X += 10000000000000
    Y += 10000000000000
    denominator = x1 * y2 - x2 * y1
    nominator = Y * x1 - X * y1
    if denominator == 0:
        raise ValueError("No solution")

    if nominator % denominator == 0:
        B = nominator // denominator
        A = (X - B * x2) // x1
        return A * 3 + B
    else:
        raise ValueError("Unhandled case")


def main():
    # inputs = read_input("sample.txt")
    inputs = read_input("input.txt")

    result = 0
    for input in inputs:
        try:
            solution = solve(*input)
            result += solution
        except ValueError as e:
            continue

    print(result)


if __name__ == "__main__":
    main()
