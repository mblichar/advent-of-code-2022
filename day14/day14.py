import sys
import operator
from collections import defaultdict

ROCK = '#'
AIR = '.'
SAND = 'o'


def add_tuples(a, b):
    return tuple(map(operator.add, a, b))


def parse_input():
    cave_map = defaultdict(lambda: AIR)
    for line in (l.rstrip('\n') for l in sys.stdin.readlines()):
        points = [[int(data) for data in token.split(',')] for token in line.split(' -> ')]
        prev_point = points[0]
        for point in points[1:]:
            if point[0] == prev_point[0]:
                for y in range(min(point[1], prev_point[1]), max(point[1], prev_point[1]) + 1):
                    cave_map[(point[0], y)] = ROCK
            else:
                for x in range(min(point[0], prev_point[0]), max(point[0], prev_point[0]) + 1):
                    cave_map[(x, point[1])] = ROCK

            prev_point = point

    return cave_map


def drop_sand(origin, cave_map_get, cave_map_set, lowest_rock):
    sand_position = origin
    while sand_position[1] <= lowest_rock:
        if cave_map_get(add_tuples(sand_position, (0, 1))) == AIR:
            sand_position = add_tuples(sand_position, (0, 1))
        elif cave_map_get(add_tuples(sand_position, (-1, 1))) == AIR:
            sand_position = add_tuples(sand_position, (-1, 1))
        elif cave_map_get(add_tuples(sand_position, (1, 1))) == AIR:
            sand_position = add_tuples(sand_position, (1, 1))
        elif sand_position == origin:
            return False
        else:
            cave_map_set(sand_position, SAND)
            return True

    return False


def main():
    is_part_two = sys.argv[1] == '2'
    cave_map = parse_input()
    lowest_rock = max(key[1] for key in cave_map.keys())
    if is_part_two:
        lowest_rock += 2

    def cave_map_get(pos):
        if is_part_two and pos[1] == lowest_rock:
            return ROCK
        else:
            return cave_map[pos]

    def cave_map_set(pos, value):
        cave_map[pos] = value

    counter = 0
    while drop_sand((500, 0), cave_map_get, cave_map_set, lowest_rock):
        counter += 1

    # add 1 for part two because sand is not infinitely going into the void but staying at origin
    print('result', counter + 1 if is_part_two else counter)


main()
