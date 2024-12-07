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
def reach(target: int, numbers: tuple[int, ...]) -> bool:
    if len(numbers) == 0:
        return target == 0

    last = numbers[-1]

    if len(str(target)) > len(str(last)) and str(target).endswith(str(last)):
        new_target = int(str(target)[: -len(str(last))])
        if reach(new_target, numbers[:-1]):
            return True

    if target % last == 0:
        if reach(target // last, numbers[:-1]):
            return True

    if target - last >= 0:
        if reach(target - last, numbers[:-1]):
            return True

    return False


def calibration_result(equations: list[Equation]) -> int:
    conditions = (reach(*eq) for eq in equations)
    targets = (target for target, _ in equations)
    return sum(t for c, t in zip(conditions, targets) if c)


def main():
    # equations = read_input("sample.txt")
    equations = read_input("input.txt")
    result = calibration_result(equations)
    print(result)


if __name__ == "__main__":
    main()
