from ast import literal_eval
from collections.abc import Iterable, Mapping
from collections import defaultdict

type Position = tuple[int, int]
type Velocity = tuple[int, int]


def read_input(filename: str) -> Iterable[tuple[Position, Velocity]]:
    def parse_line(line: str) -> tuple[Position, Velocity]:
        pos, vel = [literal_eval(x[2:]) for x in line.split()]
        return (pos, vel)

    with open(filename) as file:
        lines = [ln for line in file if (ln := line.rstrip()) != ""]
    return map(parse_line, lines)


def main():
    def final_destination(
        pos: Position,
        vel: Velocity,
    ) -> Position:
        x, y = pos
        xv, yv = vel
        x_dst = (x + xv * seconds) % x_size
        y_dst = (y + yv * seconds) % y_size
        return (x_dst, y_dst)

    def safety_factor(destinations: Mapping[Position, int]) -> int:
        x_mid = x_size // 2
        y_mid = y_size // 2

        q1, q2, q3, q4 = (0,) * 4
        for (x, y), count in destinations.items():
            if x < x_mid and y < y_mid:
                q1 += count
            if x > x_mid and y < y_mid:
                q2 += count
            if x < x_mid and y > y_mid:
                q3 += count
            if x > x_mid and y > y_mid:
                q4 += count
        return q1 * q2 * q3 * q4

    # inputs, x_size, y_size = read_input("sample.txt"), 11, 7
    inputs, x_size, y_size = read_input("input.txt"), 101, 103

    seconds = 100

    destinations: Mapping[Position, int] = defaultdict(int)

    for p, v in inputs:
        dst = final_destination(p, v)
        destinations[dst] += 1

    result = safety_factor(destinations)
    print(result)


if __name__ == "__main__":
    main()
