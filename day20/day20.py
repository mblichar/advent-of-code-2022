import sys


def parse_input():
    return list(map(lambda x: int(x), sys.stdin.readlines()))


def swap(numbers, moving_order, i, j):
    numbers[i % len(numbers)], numbers[j % len(numbers)] = numbers[j % len(numbers)], numbers[i % len(numbers)]
    moving_order[i % len(numbers)], moving_order[j % len(numbers)] = moving_order[j % len(numbers)], moving_order[
        i % len(numbers)]


def mix(numbers, moving_order):
    for order in range(len(numbers)):
        idx = moving_order.index(order)

        value = numbers[idx]

        value = abs(value) % (len(numbers) - 1)
        if numbers[idx] < 0:
            value = -value

        new_idx = (idx + value) % len(numbers)
        if value < 0 and idx + value <= 0:
            new_idx = (new_idx - 1) % len(numbers)

        if value > 0 and idx + value >= len(numbers) - 1:
            new_idx = (new_idx + 1) % len(numbers)

        if idx == new_idx:
            continue

        r = range(idx, new_idx) if idx < new_idx else range(idx - 1, new_idx - 1, -1)
        for i in r:
            swap(numbers, moving_order, i, i + 1)


def part_one():
    numbers = parse_input()
    moving_order = [i for i in range(len(numbers))]

    mix(numbers, moving_order)

    result = 0
    zero_idx = numbers.index(0)
    for offset in (1000, 2000, 3000):
        result += numbers[(zero_idx + offset) % len(numbers)]

    print('result:', result)


def part_two():
    numbers = parse_input()
    decryption_key = 811589153
    numbers = list(map(lambda x: x * decryption_key, numbers))
    moving_order = [i for i in range(len(numbers))]

    for _ in range(10):
        mix(numbers, moving_order)

    result = 0
    zero_idx = numbers.index(0)
    for offset in (1000, 2000, 3000):
        result += numbers[(zero_idx + offset) % len(numbers)]

    print('result:', result)


part_one() if sys.argv[1] == '1' else part_two()
