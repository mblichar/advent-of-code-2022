import sys
import math
import operator
from dataclasses import dataclass
from functools import reduce


@dataclass
class Monkey:
    items: [int]
    op: any
    arg_a: str
    arg_b: str
    divisor: int
    true_destination: int
    false_destination: int


def parse_monkeys():
    lines = [l.rstrip('\n') for l in sys.stdin.readlines()]
    monkeys_count = math.ceil(len(lines) / 7)
    monkeys = []

    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
    }

    for i in range(0, monkeys_count * 7, 7):
        items = [int(x) for x in (lines[i + 1].split(':'))[1].split(', ')]
        operation_tokens = (lines[i + 2].split(' = '))[1].split(' ')
        arg_a, op, arg_b = operation_tokens[0], operator_map[operation_tokens[1]], operation_tokens[2]
        divisor = int(lines[i + 3].split(' ')[-1])
        true_destination = int(lines[i + 4].split(' ')[-1])
        false_destination = int(lines[i + 5].split(' ')[-1])

        monkeys.append(Monkey(items, op, arg_a, arg_b, divisor, true_destination, false_destination))

    return monkeys


def main():
    monkeys = parse_monkeys()
    monkey_inspections = [0 for _ in monkeys]
    is_part_one = sys.argv[1] == '1'
    common_divisor = reduce(lambda x, y: x * y, (monkey.divisor for monkey in monkeys))

    for r in range(20 if is_part_one else 10000):
        for idx, monkey in enumerate(monkeys):
            while len(monkey.items) > 0:
                worry_level = monkey.items.pop(0)
                monkey_inspections[idx] += 1

                a = worry_level if monkey.arg_a == 'old' else int(monkey.arg_a)
                b = worry_level if monkey.arg_b == 'old' else int(monkey.arg_b)
                worry_level = monkey.op(a, b)

                destination = monkey.true_destination if worry_level % monkey.divisor == 0 else monkey.false_destination
                if is_part_one:
                    worry_level //= 3
                else:
                    worry_level %= common_divisor

                monkeys[destination].items.append(worry_level)

    monkey_inspections.sort()
    print(f'result: {monkey_inspections[-1] * monkey_inspections[-2]}')


main()
