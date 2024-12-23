from functools import cache
from collections import defaultdict
from heapq import heappop, heappush
from itertools import pairwise, product

type Graph = dict[str, list[tuple[str, str]]]
type PredecessorMap = Graph


def read_input(filename: str) -> list[str]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def init_grid(val, x_size, y_size):
    return [[val for _ in range(y_size)] for _ in range(x_size)]


numpad_graph = {
    "A": [("0", "<"), ("3", "^")],
    "0": [("A", ">"), ("2", "^")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("A", "v"), ("2", "<"), ("6", "^")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
}

keypad_graph = {
    "A": [("^", "<"), (">", "v")],
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
    ">": [("A", "^"), ("v", "<")],
}


def get_all_shortest_paths(start: str, end: str, graph: Graph) -> list[str]:
    infinity = 1_000_000
    pred: dict[str, list[tuple[str, str]]] = defaultdict(list)
    shortest_paths = {b: 0 if b == start else infinity for b in graph.keys()}

    visited = {start}

    queue = []
    heappush(queue, (shortest_paths[start], start))
    while len(queue) > 0:
        _, button = heappop(queue)
        visited.add(button)
        for neighbor, dir in graph[button]:
            if neighbor in visited:
                continue
            alt = shortest_paths[button] + 1
            if alt < shortest_paths[neighbor]:
                shortest_paths[neighbor] = alt
                pred[neighbor].append((button, dir))
                heappush(queue, (alt, neighbor))
            elif alt == shortest_paths[neighbor]:
                pred[neighbor].append((button, dir))

    def construct_shortest_paths(node: str, pred: PredecessorMap) -> list[str]:
        if node == start:
            return [""]

        paths = []
        for p, dir in pred[node]:
            tmp = construct_shortest_paths(p, pred)
            paths.extend(path + dir for path in tmp)

        return paths

    return [p + "A" for p in construct_shortest_paths(end, pred)]


def combine(xss: list[list[str]]) -> list[str]:
    if len(xss) == 1:
        return xss[0]

    xs, *xss = xss
    ys = combine(xss)
    return [x + y for x, y in product(xs, ys)]


def get_shortest_seq(seqs: list[str]):
    return min(zip(map(len, seqs), seqs))[1]


def get_sequence(seq: str, graph: Graph, level: int):
    shortest_paths_list = [
        get_all_shortest_paths(start, end, graph) for start, end in pairwise("A" + seq)
    ]

    combined_shortest_paths = combine(shortest_paths_list)
    if level == 0:
        return combined_shortest_paths[0]
    seqs = []
    for combined_shortest_path in combined_shortest_paths:
        seqs.append(get_sequence(combined_shortest_path, keypad_graph, level - 1))

    shortest_seq = get_shortest_seq(seqs)
    return shortest_seq


def main():
    # codes = read_input("sample.txt")
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        seq = get_sequence(code, numpad_graph, level=2)
        num = int(code[:-1])
        print(f"{len(seq)} * {num}")
        result += num * len(seq)

    print(result)


if __name__ == "__main__":
    main()
