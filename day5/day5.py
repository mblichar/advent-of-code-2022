import re
import sys


def read_initial_stacks(stack_lines):
    stacks_count_line = ' '.join(stack_lines[-1].split())  # to merge multiple whitespaces into a single one
    stacks_count = len(stacks_count_line.split(' '))
    stacks = [[] for _ in range(stacks_count)]

    # populate stacks by reading stack-related lines in opposite direction
    for line in reversed(stack_lines[:-1]):
        for index, value in enumerate(line):
            if value.isalpha():
                # it takes 4 characters to describe a single item: "[X] "
                stacks[index // 4].append(value)

    return stacks


def main():
    lines = sys.stdin.readlines()
    empty_line_index = lines.index('\n')
    stacks = read_initial_stacks(lines[:empty_line_index])

    is_part_two = sys.argv[1] == "2"

    # apply move instructions
    for line in lines[empty_line_index + 1:]:
        match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        items_count = int(match.group(1))
        source = int(match.group(2)) - 1
        destination = int(match.group(3)) - 1

        if is_part_two:
            items = stacks[source][-items_count:]
            stacks[source] = stacks[source][:-items_count]
            stacks[destination].extend(items)
        else:
            for _ in range(items_count):
                item = stacks[source].pop()
                stacks[destination].append(item)

    print(f'result: "{"".join((x[-1] if len(x) > 0 else " " for x in stacks))}"')


main()
