import sys


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
    for l in map_layout:
        print(l)

    facings = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    move_mark = ['>', 'v', '<', '^']
    row, column = 1, map_layout[1].index('.')
    facing_idx = 0
    moved_map[row][column] = move_mark[facing_idx]

    for steps, turn in moves:
        facing = facings[facing_idx]
        for _ in range(steps):
            new_row, new_column = row + facing[0], column + facing[1]
            if map_layout[new_row][new_column] == '.':
                row, column = new_row, new_column
                moved_map[row][column] = move_mark[facing_idx]
                continue

            if map_layout[new_row][new_column] == '#':
                break

            if map_layout[new_row][new_column] == ' ':
                while map_layout[new_row][new_column] == ' ':
                    new_row, new_column = (new_row + facing[0]) % len(map_layout), (new_column + facing[1]) % len(
                        map_layout[0])

                if map_layout[new_row][new_column] == '.':
                    row, column = new_row, new_column
                    moved_map[row][column] = move_mark[facing_idx]
                    continue

                if map_layout[new_row][new_column] == '#':
                    break
        if turn is not None:
            facing_idx = (facing_idx - 1) % 4 if turn == 'L' else (facing_idx + 1) % 4

    for i in range(len(map_layout)):
        for j in range(len(map_layout[0])):
            if map_layout[i][j] in (' ', '#'):
                if map_layout[i][j] != moved_map[i][j]:
                    print('invalid', map_layout[i][j], moved_map[i][j], (i, j))
    print('result:', 1000 * row + 4 * column + facing_idx)


def part_two():
    wrapping_offsets = [
        (range(1, 51), range(50, 101), 1, (0, 0))
    ]

part_one()
