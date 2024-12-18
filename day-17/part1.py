def read_input(filename: str):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(lines)


def main():
    read_input("sample.txt")


if __name__ == "__main__":
    main()
