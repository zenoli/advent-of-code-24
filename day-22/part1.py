def read_input(filename: str) -> list[int]:
    with open(filename) as file:
        lines = [int(line.rstrip()) for line in file]
    return lines  # pyright: ignore


def evolve(s: int) -> int:
    s = ((s << 6) ^ s) % (1 << 24)
    s = ((s >> 5) ^ s) % (1 << 24)
    s = ((s << 11) ^ s) % (1 << 24)
    return s


def main():
    # secrets = read_input("sample.txt")
    secrets = read_input("input.txt")

    result = 0
    for init_s in secrets:
        s = init_s
        for _ in range(2000):
            s = evolve(s)
        result += s
        print(f"{init_s}: {s}")

    print(result)


if __name__ == "__main__":
    main()
