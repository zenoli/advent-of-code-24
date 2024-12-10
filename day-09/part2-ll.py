from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import cast


def read_input(filename: str) -> str:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines[0]


@dataclass
class File:
    id: int
    start: int
    length: int
    # moved: bool = False

    next: File | None = None
    prev: File | None = None

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


def parse_files(input: str) -> tuple[File, File]:
    offset = 0

    head: File | None = None
    tail: File | None = None

    for i, c in enumerate(input):
        if i % 2 == 0:
            file = File(
                id=i // 2,
                start=offset,
                length=int(c),
            )
            if head is None or tail is None:
                head = file
                tail = file
            else:
                file.prev = tail
                tail.next = file
                tail = file
        offset += int(c)
    return cast(File, head), cast(File, tail)


def log(file: File | None):
    while file is not None:
        print(f"{file.id}: ({file.start}, {file.end})")
        file = file.next


def mv(head: File, file: File):
    curr = head
    new_head = head
    while curr.next is not None and curr != file:
        space = curr.next.start - curr.end
        if space == 0:
            new_head = curr.next

        if file.length <= space:
            if file.prev is not None:
                file.prev.next = file.next
            if file.next is not None:
                file.next.prev = file.prev
            file.start = curr.end

            file.next = curr.next
            # if curr.next is not None:
            curr.next.prev = file

            curr.next = file
            file.prev = curr

            return new_head
        else:
            curr = curr.next
    return new_head


def main():
    disk_map = read_input("sample.txt")
    # answer: 6431472344710
    # 9567304580661
    # 6431472344710
    # disk_map = read_input("input.txt")

    head, tail = parse_files(disk_map)

    order = []
    file = tail

    while True:
        order.append(file)
        if file.prev is not None:
            file = file.prev
        else:
            break

    # mv(head, tail, order[0])
    # log(head)
    # print("==================")
    # mv(head, tail, order[1])
    # log(head)
    # print("==================")
    # mv(head, tail, order[2])
    # log(head)
    # print("==================")
    # mv(head, tail, order[3])
    # log(head)
    # print("==================")
    N = len(order)
    h = head
    for i, file in enumerate(order):
        print(f"[{i}/{N}]")
        h = mv(h, file)

    log(head)

    # updated_files = copy(files)
    # N = len(files)
    # for i, f in enumerate(reversed(files)):
    #     print(f"[{i}/{N}]")
    #     updated_files = move(updated_files, f.copy)
    # log(updated_files)
    # print(sum(f.checksum for f in updated_files))
    checksum = 0
    file = head
    while file is not None:
        checksum += file.checksum
        file = file.next
    print(checksum)


if __name__ == "__main__":
    main()
