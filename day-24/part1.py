from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum, auto


class Op(StrEnum):
    XOR = auto()
    OR = auto()
    AND = auto()


class Evaluable(ABC):
    @abstractmethod
    def eval(self) -> bool:
        pass


@dataclass
class Wire(Evaluable):
    name: str
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


def main():
    inputs, gates = read_input("sample.txt")
    # inputs, gates = read_input("input.txt")

    for x in inputs.items():
        print(x)

    for x in gates.items():
        print(x)


if __name__ == "__main__":
    main()
