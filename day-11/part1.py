from functools import cache


def read_input(filename: str) -> list[int]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(map(int, lines[0].split()))


@cache
def bl(number: int, count: int) -> int:
    if count == 0:
        return 1

    if number == 0:
        return bl(1, count - 1)
    if (length := len(s := str(number))) % 2 == 0:
        h = length // 2
        return bl(int(s[:h]), count - 1) + bl(int(s[h:]), count - 1)
    return bl(number * 2024, count - 1)


def main():
    # input = read_input("sample.txt")
    input = read_input("input.txt")
    result = sum(bl(n, 75) for n in input)
    print(result)


if __name__ == "__main__":
    main()
