from ast import literal_eval
from collections.abc import Mapping
from collections import defaultdict

type Position = tuple[int, int]
type Velocity = tuple[int, int]


def read_input(filename: str) -> list[tuple[Position, Velocity]]:
    def parse_line(line: str) -> tuple[Position, Velocity]:
        pos, vel = [literal_eval(x[2:]) for x in line.split()]
        return (pos, vel)

    with open(filename) as file:
        lines = [ln for line in file if (ln := line.rstrip()) != ""]
    return list(map(parse_line, lines))


def main():
    def final_destination(
        pos: Position,
        vel: Velocity,
        seconds: int,
    ) -> Position:
        x, y = pos
        xv, yv = vel
        x_dst = (x + xv * seconds) % x_size
        y_dst = (y + yv * seconds) % y_size
        return (x_dst, y_dst)

    def get_destinations(seconds: int) -> Mapping[Position, int]:
        destinations: Mapping[Position, int] = defaultdict(int)

        for p, v in inputs:
            dst = final_destination(p, v, seconds)
            destinations[dst] += 1
        return destinations

    def compute_longest_horizontal_line(seconds: int, thresh: int):
        destinations = get_destinations(seconds)
        grid = [[False] * x_size for _ in range(y_size)]

        for pos in destinations:
            grid[pos[1]][pos[0]] = True

        longest_line = 0

        for line in grid:
            c = 0
            for x in line:
                if x:
                    c += 1
                else:
                    longest_line = max(longest_line, c)
                    c = 0

        if longest_line > thresh:
            lines = ("".join("#" if x else "." for x in line) for line in grid)
            print("\n".join(lines))

        return longest_line

    # inputs, x_size, y_size = read_input("sample.txt"), 11, 7
    inputs, x_size, y_size = read_input("input.txt"), 101, 103

    N = 1000000
    thresh = 30  # <-- magic number
    longest_line = 0
    for seconds in range(N):
        longest_line = max(
            longest_line,
            compute_longest_horizontal_line(seconds, thresh),
        )
        if longest_line > thresh:
            print(f"Found line longer than {thresh} after {seconds} seconds.")
            return

        if seconds % 100 == 0:
            print(f"[{seconds}/{N}]: Longest line: {longest_line}")


if __name__ == "__main__":
    main()
