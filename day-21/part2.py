from functools import cache
from collections import defaultdict
from heapq import heappop, heappush
from itertools import pairwise

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


@cache
def sp(start: str, end: str, level: int) -> int:
    graph = numpad_graph if {start, end} & set("0123456789") else keypad_graph
    all_sps = get_all_shortest_paths(start, end, graph)
    if level == 0:
        return len(all_sps[0])

    return min(seq_len(sp, level) for sp in all_sps)


@cache
def seq_len(seq: str, level: int) -> int:
    if level == 0:
        return len(seq)

    return sum(sp(s, e, level - 1) for s, e in pairwise("A" + seq))


def main():
    # codes = read_input("sample.txt")
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        num = int(code[:-1])
        res = seq_len(code, level=26)
        print(f"{res} * {num}")
        result += res * num

    print(result)


if __name__ == "__main__":
    main()
