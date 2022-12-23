import sys
import operator


def add_tuples(a, b):
    return tuple(map(operator.add, a, b))


def parse_input():
    elves_positions = set()

    for i, line in enumerate(sys.stdin.readlines()):
        for j, c in enumerate(line):
            if c == '#':
                elves_positions.add((i, j))

    return elves_positions


DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def run_simulation(elves_positions, max_rounds):
    round = 0
    while True:
        if max_rounds is not None and round == max_rounds:
            break

        new_elves_positions = set()
        reverse_elves_positions = dict()
        first_direction_idx = round % len(DIRECTIONS)

        some_elves_moved = False
        for position in elves_positions:
            should_move = False
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    if (x, y) != (0, 0) and add_tuples(position, (x, y)) in elves_positions:
                        should_move = True
                        break

            if not should_move:
                new_elves_positions.add(position)
                continue

            moved = False
            for j in range(len(DIRECTIONS)):
                direction = DIRECTIONS[(first_direction_idx + j) % len(DIRECTIONS)]

                can_move = True
                for offset in (-1, 0, 1):
                    check = (direction[0], offset) if direction[0] != 0 else (offset, direction[1])
                    if add_tuples(check, position) in elves_positions:
                        can_move = False
                        break

                if can_move:
                    new_position = add_tuples(position, direction)
                    if new_position in reverse_elves_positions:
                        reverse_elves_positions[new_position].append(position)
                    else:
                        reverse_elves_positions[new_position] = [position]
                    moved = True
                    some_elves_moved = True
                    break
            if not moved:
                new_elves_positions.add(position)

        for new_position, old_positions in reverse_elves_positions.items():
            if len(old_positions) == 1:
                new_elves_positions.add(new_position)
            else:
                new_elves_positions.update(old_positions)

        if not some_elves_moved:
            return elves_positions, round + 1

        elves_positions = new_elves_positions
        round += 1

    return elves_positions, round


def part_one():
    elves_positions = parse_input()
    elves_positions, _ = run_simulation(elves_positions, 10)

    elves_positions = list(elves_positions)
    position = elves_positions[0]
    max_x, min_x, max_y, min_y = position[0], position[0], position[1], position[1]
    for x, y in elves_positions[1:]:
        max_x = max(x, max_x)
        min_x = min(x, min_x)
        max_y = max(y, max_y)
        min_y = min(y, min_y)

    print('result:', (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves_positions))


def part_two():
    elves_positions = parse_input()
    _, finish_round = run_simulation(elves_positions, None)

    print('result:', finish_round)


part_one() if sys.argv[1] == '1' else part_two()
