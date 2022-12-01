import sys
import heapq
import operator

from collections import defaultdict


def find_nodes(grid, value):
    nodes = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == value:
                nodes.append((i, j))
    return nodes


def calculate_path_length(came_from, end):
    path_length = 0
    current = end
    while current in came_from:
        path_length += 1
        current = came_from[current]

    return path_length


def height(grid, pos):
    h = grid[pos[0]][pos[1]]
    if h == 'S':
        return ord('a')
    elif h == 'E':
        return ord('z')

    return ord(h)


def possible_neighbours(grid, curr, is_part_one):
    curr_height = height(grid, curr)
    for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x = tuple(map(operator.add, curr, direction))
        if 0 <= x[0] < len(grid) and 0 <= x[1] < len(grid[0]):
            allowed = height(grid, x) - curr_height <= 1 if is_part_one else curr_height - height(grid, x) <= 1
            if allowed:
                yield x


def find_shortest_path(grid):
    # A* algorithm
    start = find_nodes(grid, 'S')[0]
    end = find_nodes(grid, 'E')[0]
    part_two_ends = [start] + find_nodes(grid, 'a')

    is_part_one = sys.argv[1] == '1'

    def h(n):
        # start can be used for heuristic
        if is_part_one:
            return abs(n[0] - end[0]) + abs(n[1] - end[1])
        else:
            return min((abs(n[0] - x[0]) + abs(n[1] - x[1]) for x in part_two_ends))

    open_set = []
    g_scores = defaultdict(lambda: float('inf'))
    f_scores = defaultdict(lambda: float('inf'))
    start_node = start if is_part_one else end
    heapq.heappush(open_set, (0, start_node))
    g_scores[start_node] = 0
    f_scores[start_node] = h(start_node)
    came_from = dict()
    destination = 'E' if is_part_one else 'a'  # we want to reach closest 'a'

    while len(open_set) > 0:
        (_, curr) = heapq.heappop(open_set)
        if grid[curr[0]][curr[1]] == destination:
            return calculate_path_length(came_from, curr)

        for neighbour in possible_neighbours(grid, curr, is_part_one):
            g_score = g_scores[curr] + 1
            if g_score < g_scores[neighbour]:
                came_from[neighbour] = curr
                g_scores[neighbour] = g_score
                f_score = g_score + h(neighbour)
                f_scores[neighbour] = f_score
                heapq.heappush(open_set, (f_score, neighbour))

    return False


def main():
    grid = [r.rstrip('\n') for r in sys.stdin.readlines()]
    print(f'result: {find_shortest_path(grid)}')


main()
