type Edge = frozenset[str]


def read_input(filename: str) -> frozenset[Edge]:
    with open(filename) as file:
        lines = {frozenset(line.rstrip().split("-")) for line in file}
    return lines  # pyright: ignore


def main():
    # edges = read_input("sample.txt")
    edges = read_input("input.txt")

    nodes = set()
    for e in edges:
        nodes |= set(e)
    
    print(">>>", len(nodes))

    nodes_t = {v for v in nodes if v.startswith("t")}

    edges = set(edges)
    triplets = set()
    for v0 in nodes_t:
        for v1 in nodes - {v0}:
            for v2 in nodes - {v0, v1}:
                e0 = frozenset({v0, v1})
                e1 = frozenset({v0, v2})
                e2 = frozenset({v1, v2})
                if {e0, e1, e2} <= edges:
                    triplets.add(frozenset({v0, v1, v2}))

    for t in triplets:
        print(t)

    print(len(triplets))


if __name__ == "__main__":
    main()
