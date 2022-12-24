import sys
import heapq
import operator

BLIZZARD_TO_DIRECTION = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}


def add_tuples(a, b):
    return tuple(map(operator.add, a, b))


def sub_tuples(a, b):
    return tuple(map(operator.sub, a, b))


def mul_tuples(a, b):
    return tuple(map(operator.mul, a, b))


def parse_input():
    lines = [line.rstrip('\n') for line in sys.stdin.readlines()]

    entry = (0, lines[0].index('.'))
    exit = (len(lines) - 1, lines[-1].index('.'))
    blizzards = []

    for i, line in enumerate(lines[1:-1], 1):
        for j, c in enumerate(line):
            if c in BLIZZARD_TO_DIRECTION.keys():
                blizzards.append(((i, j), BLIZZARD_TO_DIRECTION[c]))

    return entry, exit, blizzards, len(lines) - 1, len(lines[0]) - 1


def blizzard_positions(blizzards, minute, cache, max_x, max_y):
    if minute in cache:
        return cache[minute]

    positions = set()
    for start, direction in blizzards:
        tmp = add_tuples(add_tuples(start, (-1, -1)), mul_tuples(direction, (minute, minute)))
        positions.add(add_tuples((tmp[0] % (max_x - 1), tmp[1] % (max_y - 1)), (1, 1)))

    cache[minute] = positions
    return positions


def distance(a, b):
    return sum(abs(x) for x in sub_tuples(a, b))


def find_path(entry, exit, start_minutes, blizzards, max_x, max_y):
    moves = [(0, (entry, start_minutes))]
    blizzards_cache = dict()
    current_best_result = None
    visited_positions = set()
    while len(moves) > 0:
        distance_to_exit, (position, minute) = heapq.heappop(moves)
        if (position, minute) in visited_positions:
            continue

        visited_positions.add((position, minute))

        if current_best_result is not None:
            if minute + distance_to_exit > current_best_result:
                # print('cache 2', len(moves), current_best_result)
                continue

        next_blizzard_positions = blizzard_positions(blizzards, minute + 1, blizzards_cache, max_x, max_y)
        # waiting
        if position not in next_blizzard_positions:
            heapq.heappush(moves, (distance(position, exit), (position, minute + 1)))

        for move in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new_position = add_tuples(position, move)

            if new_position == exit:
                current_best_result = minute + 1
                break

            if new_position != entry and not (0 < new_position[0] < max_x and 0 < new_position[1] < max_y):
                continue

            if new_position not in next_blizzard_positions:
                new_position_dist_to_exit = distance(new_position, exit)
                if current_best_result is None or minute + new_position_dist_to_exit < current_best_result:
                    heapq.heappush(moves, (distance(new_position, exit), (new_position, minute + 1)))

    return current_best_result - start_minutes


def part_one():
    entry, exit, blizzards, max_x, max_y = parse_input()
    print('result:', find_path(entry, exit, 0, blizzards, max_x, max_y))


def part_two():
    entry, exit, blizzards, max_x, max_y = parse_input()
    result = find_path(entry, exit, 0, blizzards, max_x, max_y)
    result += find_path(exit, entry, result, blizzards, max_x, max_y)
    result += find_path(entry, exit, result, blizzards, max_x, max_y)
    print('result:', result)


part_one() if sys.argv[1] == '1' else part_two()
