from heapq import heappop, heappush
from itertools import product

type Grid = list[str]
type Position = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def add(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Position, b: Position) -> Position:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename: str) -> Grid:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return list(lines)


def debug(grid):
    for line in grid:
        print(line)


def main():
    def get(pos: Position) -> str:
        return grid[pos[0]][pos[1]]

    def in_bounds(pos: Position) -> bool:
        return 0 <= pos[0] < x_size and 0 <= pos[1] < y_size

    def find(symbol: str) -> Position:
        for pos in product(range(x_size), range(y_size)):
            if get(pos) == symbol:
                return pos
        raise ValueError(f"Symbol {symbol} not found")

    def get_neighbors(pos: Position):
        return (
            next for dir in [UP, DOWN, LEFT, RIGHT] if get(next := add(pos, dir)) != "#"
        )

    def dijkstra(start: Position, end: Position):
        (xs, ys) = start
        (xe, ye) = end
        shortest_paths: list[list[int]] = [
            [x_size * y_size * 1000] * y_size for _ in range(x_size)
        ]
        visited: list[list[bool]] = [[False] * y_size for _ in range(x_size)]
        queue = []
        shortest_paths[xs][ys] = 0
        heappush(queue, (0, start))
        while queue:
            _, (x, y) = heappop(queue)
            if visited[x][y]:
                continue
            visited[x][y] = True

            for xn, yn in get_neighbors((x, y)):
                shortest_paths[xn][yn] = min(
                    int(shortest_paths[x][y] + 1),
                    int(shortest_paths[xn][yn]),
                )
                if not visited[xn][yn]:
                    heappush(queue, (shortest_paths[xn][yn], (xn, yn)))
        return shortest_paths[xe][ye]

    grid = read_input("sample.txt")

    x_size = len(grid)
    y_size = len(grid[0])

    start = find("S")
    end = find("E")

    debug(grid)
    shortest_path = dijkstra(start, end)
    print(shortest_path)


if __name__ == "__main__":
    main()
