def read_input(filename: str) -> tuple[list[int], ...]:
    with open(filename) as file:
        lines = [tuple(map(int, line.split())) for line in file]
    return tuple(map(list, zip(*lines)))


def main():
    # l1, l2 = read_input("sample.txt")
    l1, l2 = read_input("input.txt")
    result = sum(map(lambda x: abs(x[0] - x[1]), list(zip(sorted(l1), sorted(l2)))))
    print(result)


if __name__ == "__main__":
    main()
