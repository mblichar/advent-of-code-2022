import sys

AIR = '.'
ROCK = '#'


def can_move(cave, x, y, fields_offsets):
    for i, j in fields_offsets:
        if x + i < 0 or x + i >= len(cave) or y + j < 0 or y + j >= len(cave[0]):
            return False
        if cave[x + i][y + j] != AIR:
            return False
    return True


def run_simulation(cave, rock, highest_rock, pattern_idx, pattern, shapes_data):
    pattern_moves = {'<': (0, -1), '>': (0, 1)}

    bottom_offset, fields_offsets = shapes_data[rock % len(shapes_data)]
    x, y = highest_rock + 3 + bottom_offset, 2

    while True:
        pattern_move = pattern_moves[pattern[pattern_idx]]
        pattern_idx = (pattern_idx + 1) % len(pattern)
        if can_move(cave, x + pattern_move[0], y + pattern_move[1], fields_offsets):
            x += pattern_move[0]
            y += pattern_move[1]

        if can_move(cave, x - 1, y, fields_offsets):
            x -= 1
        else:
            break

    highest_rock = max(x, highest_rock)
    for i, j in fields_offsets:
        cave[x + i][y + j] = ROCK

    return x, y, highest_rock, pattern_idx


def find_cycle(cave, rocks_count, pattern, shapes_data):
    state_to_data = dict()

    highest_rock = -1
    pattern_idx = 0

    for rock_number in range(rocks_count):
        distance_to_rock_per_column = []
        for i in range(len(cave[0])):
            distance = 0
            for j in range(highest_rock, -1, -1):
                if cave[j][i] == ROCK:
                    break
                distance += 1
            distance_to_rock_per_column.append(distance)

        state_key = (tuple(distance_to_rock_per_column), pattern_idx, rock_number % len(shapes_data))
        if state_key in state_to_data:
            first_rock_number, first_rock_number_highest_rock = state_to_data[state_key]
            cycle_length = rock_number - first_rock_number
            cycle_added_height = highest_rock - first_rock_number_highest_rock
            return first_rock_number + 1, cycle_length, cycle_added_height

        state_to_data[state_key] = (rock_number, highest_rock)

        x, y, highest_rock, pattern_idx = run_simulation(cave, rock_number, highest_rock, pattern_idx, pattern,
                                                         shapes_data)

    # no cycle found and simulation finished, return highest_rock
    return highest_rock


def main():
    pattern = sys.stdin.readline().rstrip('\n')
    rocks_count = int(sys.argv[1])
    cave_height = 100000

    cave = [['.' for _ in range(7)] for _ in range(cave_height)]

    shapes_data = [
        (1, [(0, 0), (0, 1), (0, 2), (0, 3)]),
        (3, [(0, 1), (-1, 0), (-1, 1), (-1, 2), (-2, 1)]),
        (3, [(0, 2), (-1, 2), (-2, 0), (-2, 1), (-2, 2)]),
        (4, [(0, 0), (-1, 0), (-2, 0), (-3, 0)]),
        (2, [(0, 0), (0, 1), (-1, 0), (-1, 1)])
    ]

    cycle = find_cycle(cave, rocks_count, pattern, shapes_data)
    if type(cycle) == int:
        print('result', cycle + 1)
    else:
        print('found cycle', cycle)
        initial_rocks, cycle_length, cycle_added_height = cycle
        rocks_count_without_initial = rocks_count - initial_rocks
        cycles_count = rocks_count_without_initial // cycle_length
        minimal_rocks_count = initial_rocks + cycle_length + rocks_count_without_initial % cycle_length

        highest_rock = -1
        pattern_idx = 0
        cave = [['.' for _ in range(7)] for _ in range(cave_height)]
        for rock_number in range(minimal_rocks_count):
            x, y, highest_rock, pattern_idx = run_simulation(cave, rock_number, highest_rock, pattern_idx, pattern,
                                                             shapes_data)

        print('result', highest_rock + 1 + (cycles_count - 1) * cycle_added_height)


main()
