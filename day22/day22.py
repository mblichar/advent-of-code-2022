import sys

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)


def parse_input():
    lines = [l.rstrip('\n') for l in sys.stdin.readlines()]
    map_layout = lines[:-2]
    # to remove the need for checking if row, column is overflowing the map
    map_layout_with_borders = [' ' * (len(map_layout[0]) + 2)]
    for line in map_layout:
        map_layout_with_borders.append(' ' + line + ' ' * (len(map_layout[0]) - len(line) + 1))
    map_layout_with_borders.append(' ' * (len(map_layout[0]) + 2))
    raw_moves = lines[-1]
    moves = []
    current_move = ''
    for x in raw_moves:
        if x.isnumeric():
            current_move += x
        else:
            moves.append((int(current_move), x))
            current_move = ''
    if current_move != '':
        moves.append((int(current_move), None))  # turn doesn't matter here
    return map_layout_with_borders, moves


def part_one():
    map_layout, moves = parse_input()
    moved_map = [list(l) for l in map_layout]

    facings = [RIGHT, DOWN, LEFT, UP]
    row, column = 1, map_layout[1].index('.')
    facing_idx = 0
    for steps, turn in moves:
        facing = facings[facing_idx]
        for _ in range(steps):
            new_row, new_column = row + facing[0], column + facing[1]
            if map_layout[new_row][new_column] == '.':
                row, column = new_row, new_column
                continue
            if map_layout[new_row][new_column] == '#':
                break
            if map_layout[new_row][new_column] == ' ':
                while map_layout[new_row][new_column] == ' ':
                    new_row, new_column = (new_row + facing[0]) % len(map_layout), (new_column + facing[1]) % len(
                        map_layout[0])
                if map_layout[new_row][new_column] == '.':
                    row, column = new_row, new_column
                    continue
                if map_layout[new_row][new_column] == '#':
                    break
        if turn is not None:
            facing_idx = (facing_idx - 1) % 4 if turn == 'L' else (facing_idx + 1) % 4

    print('result:', 1000 * row + 4 * column + facing_idx)


def part_two():
    # It works only for real input, not test one
    # sides are organized in this way
    #   AB
    #   C
    #  DE
    #  F
    # below are ranges for specific sides
    side_ranges = {
        'a': (range(1, 51), range(51, 101)),
        'b': (range(1, 51), range(101, 151)),
        'c': (range(51, 101), range(51, 101)),
        'd': (range(101, 151), range(1, 51)),
        'e': (range(101, 151), range(51, 101)),
        'f': (range(151, 201), range(1, 51)),
    }
    next_side = {
        ('a', RIGHT): lambda x, y: (x, y, 'b', RIGHT),
        ('a', DOWN): lambda x, y: (x, y, 'c', DOWN),
        ('a', LEFT): lambda x, y: (151 - x, 1, 'd', RIGHT),
        ('a', UP): lambda x, y: (151 + y - 51, 1, 'f', RIGHT),
        ('b', RIGHT): lambda x, y: (151 - x, 100, 'e', LEFT),
        ('b', DOWN): lambda x, y: (51 + y - 101, 100, 'c', LEFT),
        ('b', LEFT): lambda x, y: (x, y, 'a', LEFT),
        ('b', UP): lambda x, y: (200, 1 + y - 101, 'f', UP),
        ('c', RIGHT): lambda x, y: (50, 101 + x - 51, 'b', UP),
        ('c', DOWN): lambda x, y: (x, y, 'e', DOWN),
        ('c', LEFT): lambda x, y: (101, 1 + x - 51, 'd', DOWN),
        ('c', UP): lambda x, y: (x, y, 'a', UP),
        ('d', RIGHT): lambda x, y: (x, y, 'e', RIGHT),
        ('d', DOWN): lambda x, y: (x, y, 'f', DOWN),
        ('d', LEFT): lambda x, y: (50 - x + 101, 51, 'a', RIGHT),
        ('d', UP): lambda x, y: (51 + y - 1, 51, 'c', RIGHT),
        ('e', RIGHT): lambda x, y: (50 - x + 101, 150, 'b', LEFT),
        ('e', DOWN): lambda x, y: (151 + y - 51, 50, 'f', LEFT),
        ('e', LEFT): lambda x, y: (x, y, 'd', LEFT),
        ('e', UP): lambda x, y: (x, y, 'c', UP),
        ('f', RIGHT): lambda x, y: (150, 51 + x - 151, 'e', UP),
        ('f', DOWN): lambda x, y: (1, 101 + y - 1, 'b', DOWN),
        ('f', LEFT): lambda x, y: (1, 51 + x - 151, 'a', DOWN),
        ('f', UP): lambda x, y: (x, y, 'd', UP),
    }
    map_layout, moves = parse_input()
    moved_map = [list(l) for l in map_layout]
    facings = [RIGHT, DOWN, LEFT, UP]
    row, column = 1, map_layout[1].index('.')
    facing = facings[0]
    current_side = 'a'
    current_range = side_ranges[current_side]
    for steps, turn in moves:
        for _ in range(steps):
            new_row, new_column = row + facing[0], column + facing[1]
            new_facing = facing
            new_current_side = current_side
            new_current_range = current_range
            if new_row not in current_range[0] or new_column not in current_range[1]:
                new_row, new_column, new_current_side, new_facing = next_side[(current_side, facing)](new_row,
                                                                                                      new_column)
                new_current_range = side_ranges[new_current_side]
            if map_layout[new_row][new_column] == '.':
                row, column, current_side, current_range, facing = new_row, new_column, new_current_side, new_current_range, new_facing
                continue
            if map_layout[new_row][new_column] == '#':
                break

        if turn is not None:
            facing_idx = facings.index(facing)
            facing_idx = (facing_idx - 1) % 4 if turn == 'L' else (facing_idx + 1) % 4
            facing = facings[facing_idx]

    print('result:', 1000 * row + 4 * column + facings.index(facing))


part_one() if sys.argv[1] == '1' else part_two()
