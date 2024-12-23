from collections import defaultdict

type Edge = frozenset[str]
type Graph = dict[str, set[Edge]]


def read_input(filename: str) -> frozenset[Edge]:
    with open(filename) as file:
        lines = {frozenset(line.rstrip().split("-")) for line in file}
    return lines  # pyright: ignore


def to_graphviz_format(graph):
    print("strict graph {")
    for u, vs in graph.items():
        print(f"{u} -- {','.join(vs)}")
    print("}")


def find_max_clique(v: str, graph: Graph):
    clique = {v}

    for u in graph:
        if u not in clique and clique <= graph[u]:
            clique.add(u)
    return clique


def main():
    def get_graph(edges: frozenset[Edge]) -> Graph:
        graph = defaultdict(set)
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
        return graph

    # edges = read_input("sample.txt")
    edges = read_input("input.txt")
    graph = get_graph(edges)

    max_clique = set()
    for v in graph:
        clique = find_max_clique(v, graph)
        if len(clique) > len(max_clique):
            max_clique = clique

    print(",".join(sorted(max_clique)))


if __name__ == "__main__":
    main()
