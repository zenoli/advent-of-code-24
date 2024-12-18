from heapq import heappop, heappush
from ast import literal_eval

type Grid = list[list[str]]
type Position = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def add(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Position, b: Position) -> Position:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename: str) -> list[Position]:
    def parse_line(line: str):
        return tuple(reversed(literal_eval(line)))

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(map(parse_line, lines))


def debug(grid):
    for line in grid:
        print("".join(line))


def init_grid(val, x_size, y_size):
    return [[val for _ in range(y_size)] for _ in range(x_size)]


def main():
    def get_grid(i: int) -> Grid:
        grid = init_grid(".", x_size, y_size)
        for x, y in positions[:i]:
            grid[x][y] = "#"
        return grid

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def dijkstra(grid: Grid, start: Position, end: Position):
        def get(pos: Position) -> str:
            return grid[pos[0]][pos[1]]

        (xs, ys) = start
        (xe, ye) = end
        infinity = x_size * y_size * 1000
        shortest_paths = init_grid(infinity, x_size, y_size)
        visited = init_grid(False, x_size, y_size)

        queue = []
        shortest_paths[xs][ys] = 0
        heappush(queue, (0, start))
        while queue:
            _, (x, y) = heappop(queue)
            if visited[x][y]:
                continue
            visited[x][y] = True

            for dir in {UP, DOWN, LEFT, RIGHT}:
                if in_bounds(next := add((x, y), dir)) and get(next) != "#":
                    xn, yn = next
                    shortest_paths[xn][yn] = min(
                        shortest_paths[x][y] + 1,
                        shortest_paths[xn][yn],
                    )
                    if not visited[xn][yn]:
                        heappush(queue, (shortest_paths[xn][yn], next))

        return shortest_paths[xe][ye]

    def can_reach_exit(i: int):
        grid = get_grid(i)
        infinity = x_size * y_size * 1000
        return dijkstra(grid, start, end) < infinity

    # positions, x_size, y_size = read_input("sample.txt"), 7, 7
    positions, x_size, y_size = read_input("input.txt"), 71, 71
    start = (0, 0)
    end = (x_size - 1, y_size - 1)
    N = len(positions)
    L, R = 0, N
    while R - L > 1:
        mid = (R + L) // 2
        print(f"L = {L}, R = {R}, mid = {mid}")
        if can_reach_exit(mid):
            L = mid
        else:
            R = mid

    x, y = positions[L]
    print(f"{y},{x}")


if __name__ == "__main__":
    main()
