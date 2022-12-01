import sys


def main():
    current_cycle = 0
    x_value = 1
    result = 0
    cycle_to_measure = 20
    for line in map(lambda l: l.rstrip('\n'), sys.stdin.readlines()):
        cycles_to_add = 1 if line == 'noop' else 2

        for _ in range(0, cycles_to_add):
            if abs(x_value - (current_cycle % 40)) <= 1:
                print('#', end='')
            else:
                print('.', end='')

            current_cycle += 1
            if current_cycle % 40 == 0:
                print('')  # new line

            if current_cycle == cycle_to_measure:
                result += cycle_to_measure * x_value
                cycle_to_measure += 40
                if cycle_to_measure > 220:
                    break

        if line != 'noop':
            x_value += int(line.split(' ')[1])

    print('')
    print(f'part one: {result}')


main()
