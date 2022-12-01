import sys


def chunked(l, size):
    return (l[pos:pos + size] for pos in range(0, len(l), size))


def is_in_order(left, right):
    for l, r in zip(left, right):
        if type(l) == int and type(r) == int:
            if l != r:
                return l < r
        else:
            if type(l) == int:
                l = [l]
            if type(r) == int:
                r = [r]

            result = is_in_order(l, r)
            if result is not None:
                return result

    if len(left) == len(right):
        return None  # check next input
    else:
        return len(left) < len(right)


def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - i - 1):
            if not is_in_order(items[j], items[j + 1]):
                items[j], items[j+1] = items[j+1], items[j]


def main():
    lines = list(filter(lambda l: l != '', (l.rstrip('\n') for l in sys.stdin.readlines())))
    items = [[[2]], [[6]]]  # add divider packets

    result = 0
    for idx, chunk in enumerate(chunked(lines, 2), 1):
        left, right = eval(chunk[0]), eval(chunk[1])
        items += [left, right]

        if is_in_order(left, right):
            result += idx

    print(f'part one: {result}')

    bubble_sort(items)

    print(f'part two: {(items.index([[2]]) + 1) * (items.index([[6]]) + 1)}')

main()
