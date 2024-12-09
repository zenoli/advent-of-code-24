def read_input(filename: str) -> str:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines[0]


def decode(disk_map: str) -> list[int | None]:
    res = []
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            res.extend([i // 2] * int(c))
        else:
            res.extend([None] * int(c))
    return res


def compress(input: list[int | None]) -> list[int]:
    i, j = 0, len(input) - 1
    res = []
    while i <= j:
        if input[i] is not None:
            res.append(input[i])
            i += 1
        elif input[j] is not None:
            res.append(input.pop())
            i += 1
            j -= 1
        else:
            input.pop()
            j -= 1
    return res


def checksum(input: list[int]):
    return sum(i * val for i, val in enumerate(input))


def main():
    # disk_map = read_input("sample.txt")
    disk_map = read_input("input.txt")
    print(checksum(compress(decode(disk_map))))


if __name__ == "__main__":
    main()
