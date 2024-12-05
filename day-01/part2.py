from typing import Counter


def read_input(filename: str) -> tuple[list[int], ...]:
    with open(filename) as file:
        lines = [tuple(map(int, line.split())) for line in file]
    return tuple(map(list, zip(*lines)))


def main():
    # l1, l2 = read_input("sample.txt")
    l1, l2 = read_input("input.txt")
    counts = Counter(l2)
    result = sum(x * counts[x] for x in l1)
    print(result)


if __name__ == "__main__":
    main()
