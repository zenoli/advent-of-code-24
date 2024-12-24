from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto
from collections import defaultdict


class Op(StrEnum):
    XOR = auto()
    OR = auto()
    AND = auto()


@dataclass
class Evaluable(ABC):
    name: str

    @abstractmethod
    def eval(self) -> bool:
        pass


@dataclass
class Wire(Evaluable):
    state: bool

    def eval(self):
        return self.state

    def viz(self) -> str:
        return self.name


@dataclass
class Gate(Evaluable):
    wire1: Wire | Gate
    wire2: Wire | Gate

    op: Op

    def eval(self) -> bool:
        if self.op == Op.XOR:
            return self.wire1.eval() ^ self.wire2.eval()
        if self.op == Op.OR:
            return self.wire1.eval() | self.wire2.eval()
        else:
            return self.wire1.eval() & self.wire2.eval()

    def edges(self) -> list[tuple[str, str]]:
        res = [
            (self.name, self.wire1.name),
            (self.name, self.wire2.name),
        ]
        if isinstance(self.wire1, Gate):
            res = [*res, *self.wire1.edges()]
        if isinstance(self.wire2, Gate):
            res = [*res, *self.wire2.edges()]

        return res

    def to_graphviz_format(self):
        print("strict digraph {")
        for edge in self.edges():
            print(" -> ".join(edge))
        print("}")


def read_input(filename: str):
    inputs: dict[str, int] = {}
    gates: dict[str, tuple[str, str, str]] = {}
    with open(filename) as file:
        parse_inputs = True
        for line in file:
            line = line.rstrip()
            if line == "":
                parse_inputs = False
                continue

            if parse_inputs:
                splits = line.split(":")
                wire, state = splits[0], int(splits[1].strip())
                inputs[wire] = state
            else:
                wire1, op, wire2, _, out_wire = line.split()
                gates[out_wire] = (wire1, op, wire2)

    return inputs, gates


def to_number(outputs: list[bool]):
    return int("".join(str(int(b)) for b in outputs), 2)


def to_graphviz_format(graph):
    def vertex(v):
        return f'"{v}"'

    print("strict digraph {")
    for v, edges in graph.items():
        u1, u2, op = edges
        color: str
        if op == "XOR":
            color = "red"
        elif op == "AND":
            color = "blue"
        else:
            color = "yellow"
        # for u1 in edges:
        print(f'{vertex(v)} [color="{color}"]')
        print(f"{vertex(v)} -> {vertex(u1)}")
        print(f"{vertex(v)} -> {vertex(u2)}")
        # print(f"{vertex(v)} -> {vertex(u)}")
    print("}")


def to_graph(gates: dict[str, tuple[str, str, str]]):
    graph = defaultdict(list)
    for v, (wire1, op, wire2) in gates.items():
        graph[f"{v}"].extend([wire1, wire2, op])
        # graph[f"{v} ({op})"].extend([wire1, wire2])
    return graph


def main():
    def init(name: str):
        if name[0] in "xy":
            return Wire(name=name, state=bool(inputs[name]))
        wire1, op, wire2 = gates[name]
        return Gate(
            name=name,
            wire1=init(wire1),
            wire2=init(wire2),
            op=Op(op.lower()),
        )

    # inputs, gates = read_input("sample.txt")
    inputs, gates = read_input("input-z35-fix.txt")
    # inputs, gates = read_input("input-mod.txt")

    graph = to_graph(gates)
    to_graphviz_format(graph)
    # outputs = list(reversed(sorted(name for name in gates if name.startswith("z"))))
    # out_gates = [init(output) for output in outputs]
    # out_gates[0].to_graphviz_format()
    # result = [o.eval() for o in out_gates]
    # print(to_number(result))

    # >> correct: (dpg, z25), (z10, kmb), (tpv, z15), (mmf, vdk)
    # >> correct: ["dpg", "z25", "z10", "kmb", "tvp", "z15", "mmf", "vdk" ]


if __name__ == "__main__":
    main()
