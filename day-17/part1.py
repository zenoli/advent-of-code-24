from dataclasses import dataclass
import sys


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


def main():
    def combo(x) -> int:
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

    def adv(x):
        state.A = state.A // (1 << combo(x))
        state.ip += 2

    def bxl(x):
        state.B = state.B ^ x
        state.ip += 2

    def bst(x):
        state.B = combo(x) % 8
        state.ip += 2

    def jnz(x):
        if state.A == 0:
            state.ip += 2
        else:
            state.ip = x

    def bxc(_):
        state.B = state.B ^ state.C
        state.ip += 2

    def out(x):
        # print(combo(x) % 8, end=",")
        print(combo(x) % 8, end=",", flush=True)
        state.ip += 2

    def bdv(x):
        state.B = state.A // (1 << combo(x))
        state.ip += 2

    def cdv(x):
        state.C = state.A // (1 << combo(x))
        state.ip += 2

    def step(opcode: int, operand):
        return instructions[opcode](operand)

    def run():
        N = len(program)
        while state.ip < N:
            opcode = program[state.ip]
            operand = program[state.ip + 1]
            step(opcode, operand)
        sys.stdout.write("\b")  # move back the cursor
        sys.stdout.write(" \n")

    # registers, program = read_input("sample.txt")
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
    state = State(A, B, C)
    run()


if __name__ == "__main__":
    main()
