import sys
import operator


def add_tuples(a, b):
    return tuple(map(operator.add, a, b))


def sub_tuples(a, b):
    return tuple(map(operator.sub, a, b))


def draw_map(knots, size):
    for x in range(size // 2, -(size // 2 + 1), -1):
        line = []
        for y in range(-size // 2, size // 2 + 1):
            index = knots.index((x, y)) if (x, y) in knots else None
            if index == 0:
                line.append('H')
            elif index is not None:
                line.append(str(index))
            elif (x, y) == (0, 0):
                line.append('s')
            else:
                line.append('.')
        print(''.join(line))

    print('')


def update_knot_position(prev, current):
    diff = sub_tuples(prev, current)
    if abs(diff[0]) < 2 and abs(diff[1]) < 2:
        return current

    correction_x = -1 if diff[0] > 0 else 1
    correction_y = -1 if diff[1] > 0 else 1
    if diff[0] == 0:
        current = (current[0], prev[1] + correction_y)
    elif diff[1] == 0:
        current = (prev[0] + correction_x, current[1])
    elif abs(diff[0]) > abs(diff[1]):
        current = (prev[0] + correction_x, prev[1])
    elif abs(diff[0]) < abs(diff[1]):
        current = (prev[0], prev[1] + correction_y)
    elif abs(diff[0]) == abs(diff[1]):
        current = (prev[0] + correction_x, prev[1] + correction_y)

    return current


def main():
    direction_to_move = {
        'R': (0, 1),
        'L': (0, -1),
        'U': (1, 0),
        'D': (-1, 0)
    }
    knots = [(0, 0) for _ in range(int(sys.argv[1]))]
    tail_visited_positions = {knots[-1]}

    for line in sys.stdin.readlines():
        direction, steps = line.rstrip('\n').split(' ')

        for _ in range(int(steps)):
            knots[0] = add_tuples(knots[0], direction_to_move[direction])

            for i in range(1, len(knots)):
                knots[i] = update_knot_position(knots[i - 1], knots[i])

            tail_visited_positions.add(knots[-1])

    print(f'result: {len(tail_visited_positions)}')


main()
