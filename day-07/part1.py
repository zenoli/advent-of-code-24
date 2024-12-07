from functools import cache

type Equation = tuple[int, tuple[int, ...]]


def read_input(filename: str) -> list[Equation]:
    def parse_equation(line: str) -> Equation:
        target, numbers = line.split(":")
        return int(target), tuple(map(int, numbers.split()))

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(map(parse_equation, lines))


@cache
def reach(target: int, numbers: tuple[int]) -> bool:
    if numbers == tuple():
        return target == 0

    reach_div, reach_mul = False, False
    last = numbers[-1]

    if target % last == 0:
        reach_div = reach(target // last, numbers[:-1])
    if target - last >= 0:
        reach_mul = reach(target - last, numbers[:-1])

    return reach_div or reach_mul


def main():
    # equations = read_input("sample.txt")
    equations = read_input("input.txt")
    conditions = (reach(*eq) for eq in equations)
    targets = (target for target, _ in equations)
    result = sum(t for c, t in zip(conditions, targets) if c)
    print(result)


if __name__ == "__main__":
    main()
