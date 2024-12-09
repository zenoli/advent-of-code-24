from dataclasses import dataclass
from itertools import pairwise


def read_input(filename: str) -> str:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines[0]


@dataclass
class File:
    id: int
    start: int
    length: int

    @property
    def interval(self) -> range:
        return range(self.start, self.end)

    @property
    def end(self) -> int:
        return self.start + self.length

    @property
    def checksum(self) -> int:
        return self.id * sum(self.interval)

    @property
    def copy(self):
        return File(id=self.id, start=self.start, length=self.length)


def parse_files(input: str) -> list[File]:
    files = []
    offset = 0

    for i, c in enumerate(input):
        if i % 2 == 0:
            files.append(
                File(
                    id=i // 2,
                    start=offset,
                    length=int(c),
                )
            )
        offset += int(c)
    return files


def move(files: list[File], f: File) -> list[File]:
    out_files = []
    inserted = False
    for f1, f2 in pairwise(files):
        if out_files == []:
            out_files.append(f1)

        space = f2.start - f1.end
        if not inserted and f.length <= space and f1.end < f.end:
            out_files.append(File(id=f.id, start=f1.end, length=f.length))
            inserted = True
        if f.id == f2.id and inserted:
            continue
        out_files.append(f2)

    return out_files


def copy(files: list[File]) -> list[File]:
    return [f.copy for f in files]


def log(files: list[File]):
    for file in files:
        print(f"{file.id}: ({file.start}, {file.end})")


def main():
    # disk_map = read_input("sample.txt")
    # answer: 6431472344710
    disk_map = read_input("input.txt")

    files = parse_files(disk_map)

    updated_files = copy(files)
    N = len(files)
    for i, f in enumerate(reversed(files)):
        print(f"[{i}/{N}]")
        updated_files = move(updated_files, f.copy)
    log(updated_files)
    print(sum(f.checksum for f in updated_files))


if __name__ == "__main__":
    main()
