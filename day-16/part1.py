from heapq import heappop, heappush
from itertools import product

type Grid = list[str]
type Position = tuple[int, int]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


directions = {UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3}


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

    def dijkstra(start: Position, end: Position):
        (xs, ys) = start
        (xe, ye) = end
        infinity = x_size * y_size * 1000
        shortest_paths = [
            [[infinity] * len(directions) for _ in range(y_size)] for _ in range(x_size)
        ]
        visited = [
            [[False] * len(directions) for _ in range(y_size)] for _ in range(x_size)
        ]

        queue = []
        shortest_paths[xs][ys][directions[RIGHT]] = 0
        heappush(queue, (0, (start, RIGHT)))
        while queue:
            _, ((x, y), dir) = heappop(queue)
            if visited[x][y][directions[dir]]:
                continue
            visited[x][y][directions[dir]] = True

            if in_bounds(next := add((x, y), dir)) and get(next) != "#":
                xn, yn = next
                shortest_paths[xn][yn][directions[dir]] = min(
                    int(shortest_paths[x][y][directions[dir]] + 1),
                    int(shortest_paths[xn][yn][directions[dir]]),
                )
                if not visited[xn][yn][directions[dir]]:
                    heappush(
                        queue,
                        (shortest_paths[xn][yn][directions[dir]], ((xn, yn), dir)),
                    )

            for dir_n in directions.keys():
                shortest_paths[x][y][directions[dir_n]] = min(
                    int(shortest_paths[x][y][directions[dir]] + 1000),
                    int(shortest_paths[x][y][directions[dir_n]]),
                )
                if not visited[x][y][directions[dir_n]]:
                    heappush(
                        queue,
                        (shortest_paths[x][y][directions[dir_n]], ((x, y), dir_n)),
                    )

        return shortest_paths[xe][ye]

    # grid = read_input("sample.txt")
    grid = read_input("input.txt")

    x_size = len(grid)
    y_size = len(grid[0])

    start = find("S")
    end = find("E")

    debug(grid)
    shortest_path = dijkstra(start, end)
    print(min(shortest_path))


if __name__ == "__main__":
    main()
