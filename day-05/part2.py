from itertools import groupby, combinations, chain
from functools import cmp_to_key

type Rule = tuple[int, ...]
type Page = list[int]


def read_input(filename: str) -> tuple[set[Rule], list[Page]]:
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    rules_input, pages_input = [
        list(group) for key, group in groupby(lines, key=lambda x: x == "") if not key
    ]

    def parse_rule(rule: str) -> Rule:
        return tuple(map(int, rule.split("|")))

    def parse_page(page: str) -> Page:
        return list(map(int, page.split(",")))

    rules = set(map(parse_rule, rules_input))
    pages = list(map(parse_page, pages_input))

    return rules, pages


def validate(page: Page, rules: set[Rule]):
    return set(combinations(page, 2)).issubset(rules)


def median(page: Page):
    return page[len(page) // 2]


def get_numbers(rules: set[Rule]):
    return set(chain.from_iterable(rules))


def is_connected(rules: set[Rule]) -> bool:
    """Verify that the every tuple of numbers is comparable."""
    return len(rules) == len(list(combinations(get_numbers(rules), 2)))


def main():
    # rules, pages = read_input("sample.txt")
    rules, pages = read_input("input.txt")

    assert is_connected(rules)

    def cmp(x: int, y: int) -> int:
        if x == y:
            return 0
        if (x, y) in rules:
            return -1
        else:
            return 1

    result = sum(
        median(sorted(page, key=cmp_to_key(cmp)))
        for page in pages
        if not validate(page, rules)
    )
    print(result)


if __name__ == "__main__":
    main()
