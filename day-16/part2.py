from collections import defaultdict
from collections.abc import Mapping
from heapq import heappop, heappush
from itertools import product

type Grid = list[str]
type Position = tuple[int, int]
type Direction = tuple[int, int]
type State = tuple[Position, Direction]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


directions = {UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3}
directions_inv = dict((v, k) for k, v in directions.items())


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
        pred: Mapping[State, list[State]] = defaultdict(list)
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
                alt = shortest_paths[x][y][directions[dir]] + 1
                cur = shortest_paths[xn][yn][directions[dir]]
                if alt < cur:
                    pred[((xn, yn), dir)] = [((x, y), dir)]
                elif alt == cur:
                    pred[((xn, yn), dir)].append(((x, y), dir))

                shortest_paths[xn][yn][directions[dir]] = min(alt, cur)
                if not visited[xn][yn][directions[dir]]:
                    heappush(
                        queue,
                        (shortest_paths[xn][yn][directions[dir]], ((xn, yn), dir)),
                    )

            for dir_n in directions.keys():
                alt = shortest_paths[x][y][directions[dir]] + 1000
                cur = shortest_paths[x][y][directions[dir_n]]
                if alt < cur:
                    pred[((x, y), dir_n)] = [((x, y), dir)]
                elif alt == cur:
                    pred[((x, y), dir_n)].append(((x, y), dir))

                shortest_paths[x][y][directions[dir_n]] = min(alt, cur)
                if not visited[x][y][directions[dir_n]]:
                    heappush(
                        queue,
                        (shortest_paths[x][y][directions[dir_n]], ((x, y), dir_n)),
                    )

        min_path = min(shortest_paths[xe][ye])
        return (
            [
                (directions_inv[i], path_length)
                for i, path_length in enumerate(shortest_paths[xe][ye])
                if path_length == min_path
            ],
            pred,
        )

    def traverse(state: State):
        pos, dir = state
        result.add(pos)
        for prev in pred_map[state]:
            traverse(prev)

    # grid = read_input("sample.txt")
    grid = read_input("input.txt")

    x_size = len(grid)
    y_size = len(grid[0])

    start = find("S")
    end = find("E")

    debug(grid)
    shortest_path, pred_map = dijkstra(start, end)
    print(shortest_path)

    result: set[Position] = set()

    for dir, _ in shortest_path:
        traverse((end, dir))

    print(len(result))


if __name__ == "__main__":
    main()
