import re
from ast import literal_eval


def read_input(filename: str) -> str:
    with open(filename) as file:
        lines = [line for line in file]
    return "".join(lines)


def solve(line):
    matches = re.findall(r"(?<=mul)\(\d+,\d+\)|don't\(\)|do\(\)", line)

    result = 0
    state = True
    for match in matches:
        if match == "don't()":
            state = False
        elif match == "do()":
            state = True
        elif state:
            x, y = literal_eval(match)
            result += x * y
    return result


def main():
    # lines = read_input("sample.txt")
    line = read_input("input.txt")
    result = solve(line)
    print(result)


if __name__ == "__main__":
    main()
