import sys
import operator
from collections import namedtuple
from decimal import Decimal

MonkeyData = namedtuple('MonkeyData', ['value', 'operation', 'monkey_a', 'monkey_b'])


def parse_input():
    monkeys = dict()

    for line in sys.stdin.readlines():
        monkey_name, rest = line.strip().split(': ')
        rest = rest.split(' ')

        if len(rest) == 1:
            monkeys[monkey_name] = MonkeyData(Decimal(rest[0]), None, None, None)
        else:
            monkeys[monkey_name] = MonkeyData(None, rest[1], rest[0], rest[2])

    return monkeys


def get_monkey_result(monkeys, start_monkey):
    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    monkeys_result = dict()
    monkeys_to_check = [start_monkey]

    while len(monkeys_to_check) > 0:
        monkey_name = monkeys_to_check.pop()
        monkey_data = monkeys[monkey_name]

        if monkey_data.value is not None:
            monkeys_result[monkey_name] = monkey_data.value
            continue

        if monkey_name in monkeys_result:
            print('should not happen')
            continue

        missing_monkey_results = []
        for name in (monkey_data.monkey_a, monkey_data.monkey_b):
            if name not in monkeys_result:
                if monkeys[name].value is not None:
                    monkeys_result[name] = monkeys[name].value
                else:
                    missing_monkey_results.append(name)

        if len(missing_monkey_results) == 0:
            a_result = monkeys_result[monkey_data.monkey_a]
            b_result = monkeys_result[monkey_data.monkey_b]

            if type(a_result) != str and type(b_result) != str:
                monkeys_result[monkey_name] = operator_map[monkey_data.operation](monkeys_result[monkey_data.monkey_a],
                                                                                  monkeys_result[monkey_data.monkey_b])
            else:
                monkeys_result[monkey_name] = f'{monkey_data.operation} {a_result} {b_result}'
        else:
            monkeys_to_check.append(monkey_name)  # to recalculate the result after missing monkeys are calculated
            monkeys_to_check += missing_monkey_results

    return monkeys_result[start_monkey]


def solve_equation(left_side, right_side):
    result = right_side
    operator_map = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    reverse_operator_map = {
        '+': operator.sub,
        '-': operator.add,
        '*': operator.truediv,
        '/': operator.mul,
    }

    tokens = left_side.split(' ')
    operators_and_x = list(operator_map.keys()) + ['x']

    while len(tokens) > 1:
        if tokens[1] in operators_and_x:
            arg = Decimal(tokens[-1])
            result = reverse_operator_map[tokens[0]](result, arg)
            tokens = tokens[1:-1]
        else:
            arg = Decimal(tokens[1])
            if tokens[0] in ('-', '/'):
                result = operator_map[tokens[0]](arg, result)
            else:
                result = reverse_operator_map[tokens[0]](result, arg)
            tokens = tokens[2:]

    return result


def part_one():
    monkeys = parse_input()
    print('result:', get_monkey_result(monkeys, 'root'))


def part_two():
    monkeys = parse_input()
    root_a = monkeys['root'].monkey_a
    root_b = monkeys['root'].monkey_b
    monkeys['humn'] = MonkeyData('x', None, None, None)
    a_result = get_monkey_result(monkeys, root_a)
    b_result = get_monkey_result(monkeys, root_b)

    result = solve_equation(a_result, b_result) if type(a_result) == str else solve_equation(b_result, a_result)
    print('result:', result)


part_one() if sys.argv[1] == '1' else part_two()
