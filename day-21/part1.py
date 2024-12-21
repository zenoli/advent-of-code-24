from heapq import heappop, heappush
from itertools import pairwise


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
    ">": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
}


def get_btn_presses(start: str, end: str, graph: dict[str, list[tuple[str, str]]]):
    infinity = 1000
    pred = {}
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
                pred[neighbor] = (button, dir)
                heappush(queue, (alt, neighbor))

    next = end
    btn_presses = ""
    while next != start:
        next, d = pred[next]
        btn_presses = d + btn_presses
    return btn_presses


def get_numpad_sequence(code: str):
    return (
        "A".join(
            get_btn_presses(start, end, numpad_graph)
            for start, end in pairwise("A" + code)
        )
        + "A"
    )


def main():
    codes = read_input("sample.txt")
    sequence = get_numpad_sequence("029A")
    assert sequence == "<A^A>^^AvvvA"
    print(sequence)


if __name__ == "__main__":
    main()
