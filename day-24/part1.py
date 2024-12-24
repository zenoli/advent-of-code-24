from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto


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
    inputs, gates = read_input("input.txt")

    outputs = list(reversed(sorted(name for name in gates if name.startswith("z"))))
    out_gates = [init(output) for output in outputs]
    result = [o.eval() for o in out_gates]
    print(to_number(result))


if __name__ == "__main__":
    main()
