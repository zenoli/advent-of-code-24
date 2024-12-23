import sys
from dataclasses import dataclass
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

    def input_program(A_in: int):
        def combo(x):
            if x <= 3:
                return x
            if x == 4:
                return A
            if x == 5:
                return B
            if x == 6:
                return C
            else:
                raise ValueError(f"{x} is not a valid combo operand.")

        out = []

        A = A_in
        B = 0
        C = 0

        while True:
            # 2,4: bst(4)
            B = A % 8
            # 1,5: bxl(5)
            B = B ^ 0b101
            # 7,5: cdv(5)
            C = A // (1 << B)
            # 1,6: bxl(6)
            B = B ^ 0b110
            # 4,3: bxc()
            B = B ^ C
            # 5,5: out(5)
            out += str(B % 8)
            # 0,3: adv(3)
            A = A // 8
            # 3,0
            if A == 0:
                return out

    def dec(oct: int):
        return int(str(oct), 8)

    def step(state: State) -> State:
        opcode = program[state.ip]
        operand = program[state.ip + 1]
        res = instructions[opcode](operand, state)
        # print(f"A = {bin(res.A)}, B = {bin(res.B)}, C = {bin(res.C)}")
        # print(f"A = {oct(res.A)}, B = {oct(res.B)}, C = {oct(res.C)}")
        return res

    def run(state: State) -> State:
        N = len(program)
        while state.ip < N:
            state = step(state)
        return state

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
    # registers, program = read_input("sample.txt")
    # registers, program = read_input("sample-part2.txt")
    registers, program = read_input("input.txt")
    A, B, C = registers

    d = defaultdict(int)
    N = 1000
    A = 1

    # for A in range(dec(7777)):
    #     out_state = run(State(A, 0, 0))
    #     d = int(out_state.out.replace(",", ""))
    #     print(out_state.out)
    A_oct = int(sys.argv[1])
    A_dec = dec(A_oct)
    print("NEW", ",".join(input_program(A_dec)))
    # print(A_oct, A_dec)
    state = State(A_dec, B, C)
    out_state = run(state)
    prg_out = ",".join(map(str, program))
    print("OUT", out_state.out[1:])
    print("PRG", prg_out)

    # print(A_oct)
    # d[len(out_state.out) // 2] += 1
    # print("P", out_state.out)
    # print("O", prg_out)
    # print(A, A % 8, out_state.out)
    # print("1" + i * "0", out_state.out)
    # if prg_out == out_state.out:
    #     print("Found:", A)
    #     return
    # A *= 8


if __name__ == "__main__":
    main()
