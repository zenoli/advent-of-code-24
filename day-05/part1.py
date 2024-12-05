from itertools import groupby, combinations

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


def main():
    # rules, pages = read_input("sample.txt")
    rules, pages = read_input("input.txt")

    result = sum(median(page) for page in pages if validate(page, rules))
    print(result)


if __name__ == "__main__":
    main()
