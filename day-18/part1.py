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
    def get_grid(positions: list[Position], x_size: int, y_size: int) -> Grid:
        grid = init_grid(".", x_size, y_size)
        for x, y in positions:
            grid[x][y] = "#"
        return grid

    def get(pos: Position) -> str:
        return grid[pos[0]][pos[1]]

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def dijkstra(start: Position, end: Position):
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

    # positions, x_size, y_size, b = read_input("sample.txt"), 7, 7, 12
    positions, x_size, y_size, b = read_input("input.txt"), 71, 71, 1024
    grid = get_grid(positions[:b], x_size, y_size)

    start = (0, 0)
    end = (x_size - 1, y_size - 1)

    debug(grid)
    result = dijkstra(start, end)
    print(result)


if __name__ == "__main__":
    main()
