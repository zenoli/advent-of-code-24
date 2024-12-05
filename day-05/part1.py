def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def main():
    lines = read_input("sample.txt")


if __name__ == "__main__":
    main()
