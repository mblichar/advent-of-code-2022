import sys


def part_one():
    points = set(tuple(map(lambda x: int(x), line.rstrip('\n').split(','))) for line in sys.stdin.readlines())

    result = 0
    for x, y, z in points:
        for i, j, k in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]:
            if (x + i, y + j, z + k) not in points:
                result += 1

    print('result:', result)


DIRECTIONS = [(0, 1), (1, 1), (2, 1), (0, -1), (1, -1), (2, -1)]


def is_point_a_bubble(start_point, points, max_per_dir, min_per_dir, bubble_state_cache):
    points_to_check = [start_point]
    visited_points = set()

    is_bubble = True
    while len(points_to_check) > 0:
        point = points_to_check.pop()
        visited_points.add(point)

        if point in bubble_state_cache:
            if bubble_state_cache[point]:
                break
            else:
                is_bubble = False
                break

        if point <= min_per_dir or point >= max_per_dir:
            is_bubble = False
            break

        for idx, direction in DIRECTIONS:
            new_point = list(point)
            new_point[idx] += direction
            new_point = tuple(new_point)

            stop = new_point[idx] < min_per_dir[idx] if direction < 0 else new_point[idx] > max_per_dir[idx]
            if not stop and new_point not in points and new_point not in visited_points:
                points_to_check.append(new_point)

    for point in visited_points:
        bubble_state_cache[point] = is_bubble

    return is_bubble


def part_two():
    points = list(tuple(map(lambda x: int(x), line.rstrip('\n').split(','))) for line in sys.stdin.readlines())

    max_per_dir = list(points[0])
    min_per_dir = list(points[0])

    points = set(points)

    for point in points:
        for idx, coord in enumerate(point):
            # +1/-1 to store max/min coords for first non-rock position
            max_per_dir[idx] = max(max_per_dir[idx] + 1, coord)
            min_per_dir[idx] = min(min_per_dir[idx] - 1, coord)

    max_per_dir = tuple(max_per_dir)
    min_per_dir = tuple(min_per_dir)
    result = 0
    bubble_state_cache = dict()

    for point in points:
        for idx, direction in DIRECTIONS:
            point_to_check = list(point)
            point_to_check[idx] += direction
            point_to_check = tuple(point_to_check)

            if point_to_check not in points:
                if not is_point_a_bubble(point_to_check, points, max_per_dir, min_per_dir, bubble_state_cache):
                    result += 1

    print('result:', result)


part_one() if sys.argv[1] == '1' else part_two()
