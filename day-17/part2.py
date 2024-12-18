from dataclasses import dataclass
from functools import cache
from collections import defaultdict


def read_input(filename: str):
    def parse_lines(lines: list[str]):
        def parse_register(line: str):
            return int(line.split(" ")[2])

        line_a, line_b, line_c, _, program = lines
        registers = map(parse_register, [line_a, line_b, line_c])
        program = map(int, program.split(" ")[1].split(","))
        return list(registers), list(program)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return parse_lines(list(lines))


@dataclass
class State:
    A: int
    B: int
    C: int
    ip: int = 0
    out: str = ""


def main():
    def combo(x, state: State) -> int:
        if x in range(4):
            return x
        if x == 4:
            return state.A
        if x == 5:
            return state.B
        if x == 6:
            return state.C
        else:
            raise ValueError(f"{x} is not a valid combo operand.")

    def adv(x, state: State) -> State:
        return State(
            A=state.A // (1 << combo(x, state)),
            B=state.B,
            C=state.C,
            ip=state.ip + 2,
            out=state.out,
        )

    def bxl(x, state: State) -> State:
        return State(
            A=state.A,
            B=state.B ^ x,
            C=state.C,
            ip=state.ip + 2,
            out=state.out,
        )

    def bst(x, state: State) -> State:
        return State(
            A=state.A,
            B=combo(x, state) % 8,
            C=state.C,
            ip=state.ip + 2,
            out=state.out,
        )

    def jnz(x, state: State) -> State:
        return State(
            A=state.A,
            B=state.B,
            C=state.C,
            ip=(state.ip + 2) if state.A == 0 else x,
            out=state.out,
        )

    def bxc(_, state: State) -> State:
        return State(
            A=state.A,
            B=state.B ^ state.C,
            C=state.C,
            ip=state.ip + 2,
            out=state.out,
        )

    def out(x, state: State) -> State:
        return State(
            A=state.A,
            B=state.B,
            C=state.C,
            ip=state.ip + 2,
            out=f"{state.out},{combo(x, state) % 8}",
        )

    def bdv(x, state: State) -> State:
        return State(
            A=state.A,
            B=state.A // (1 << combo(x, state)),
            C=state.C,
            ip=state.ip + 2,
            out=state.out,
        )

    def cdv(x, state: State) -> State:
        return State(
            A=state.A,
            B=state.B,
            C=state.A // (1 << combo(x, state)),
            ip=state.ip + 2,
            out=state.out,
        )

    def step(state: State) -> State:
        opcode = program[state.ip]
        operand = program[state.ip + 1]
        return instructions[opcode](operand, state)

    def run(state: State) -> State:
        N = len(program)
        while state.ip < N:
            state = step(state)
        return state

    # registers, program = read_input("sample.txt")
    # registers, program = read_input("sample-part2.txt")
    registers, program = read_input("input.txt")
    A, B, C = registers

    instructions = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    d = defaultdict(int)
    N = 112210000000000
    # for A in range(1000):
    #     state = State(A, B, C)
    #     out_state = run(state)
    #     d[len(out_state.out) // 2] += 1
    #     prg_out = "," + ",".join(map(str, program))
    #     # print("P", out_state.out)
    #     # print("O", prg_out)
    #     # print(A, A % 8, out_state.out)
    #     print(out_state)
    #     if prg_out == out_state.out:
    #         print("Found:", A)
    #         return
    # print(d)

    count = 0
    limit = 100

    # A = 1
    # while count < 10:
    #     out_state = run(State(A+2, B, C))
    #     print(out_state.out)
    #     A *= 8
    #     count += 1

    # for i in range(8):
    #     program = [5, 6]
    #     out_state = run(State(i, i, i))
    #     print(out_state.out)
    #     assert int(out_state.out[1]) == i
    # program = [0, 3, 5, 4, 3, 0]

    prg_out = "," + ",".join(map(str, program))
    for A in range(56 * 7**14, 56 * 7**16):
        out_state = run(State(A, 0, 0))
        print(out_state.out)
        print(prg_out)
        if out_state.out == prg_out:
            return

    # print("," + ",".join(map(str, program)))


if __name__ == "__main__":
    main()
