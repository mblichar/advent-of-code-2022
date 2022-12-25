import sys

VALUE = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}


def part_one():
    decimal_result = 0
    for line in (l.rstrip('\n') for l in sys.stdin.readlines()):
        for i, c in enumerate(reversed(line), 0):
            decimal_result += (5 ** i) * VALUE[c]

    result = []
    while decimal_result != 0:
        rest = decimal_result % 5
        if 0 <= rest <= 2:
            result.append(str(rest))
            decimal_result //= 5
        else:
            result.append('-' if rest == 4 else '=')
            decimal_result = (decimal_result + 5 - rest) // 5

    print('result', ''.join(reversed(result)))


part_one()
