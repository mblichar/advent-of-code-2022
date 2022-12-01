import sys
from itertools import chain
from functools import reduce

TOP = 'top'
RIGHT = 'right'
BOTTOM = 'bottom'
LEFT = 'left'


def new_visibility():
    return {
        TOP: False,
        RIGHT: False,
        BOTTOM: False,
        LEFT: False
    }


def new_score():
    return {
        TOP: 0,
        RIGHT: 0,
        BOTTOM: 0,
        LEFT: 0
    }


def main():
    lines = sys.stdin.readlines()
    grid = [[int(x) for x in line.rstrip('\n')] for line in lines]
    visibility = [[new_visibility() for _ in range(len(row))] for row in grid]
    scores = [[new_score() for _ in range(len(row))] for row in grid]

    # set visibility on edges
    for x in range(len(grid)):
        visibility[x][0][LEFT] = True
        visibility[x][-1][RIGHT] = True

    for x in range(len(grid[0])):
        visibility[0][x][TOP] = True
        visibility[-1][x][BOTTOM] = True

    last_visible_height = {
        TOP: 0,
        RIGHT: 0,
        BOTTOM: 0,
        LEFT: 0
    }

    def dir_to_prev_range(direction, r, c):
        if direction == TOP:
            return ((x, c) for x in range(r - 1, -1, -1))

        if direction == RIGHT:
            return ((r, x) for x in range(c + 1, len(grid[0])))

        if direction == LEFT:
            return ((r, x) for x in range(c - 1, -1, -1))

        if direction == BOTTOM:
            return ((x, c) for x in range(r + 1, len(grid)))

    def update_visibility_and_scores(direction, r, c):
        nonlocal grid
        nonlocal visibility
        nonlocal scores
        nonlocal last_visible_height

        visibility[r][c][direction] = grid[r][c] > last_visible_height[direction]
        if visibility[r][c][direction]:
            last_visible_height[direction] = grid[r][c]

        for prev_r, prev_c in dir_to_prev_range(direction, r, c):
            scores[r][c][direction] += 1

            if grid[prev_r][prev_c] >= grid[r][c]:
                break

    # go through rows in both direction, no need to calculate scores on the edges because they would always be 0
    for r in range(1, len(grid) - 1):
        last_visible_height[LEFT] = grid[r][0]
        last_visible_height[RIGHT] = grid[r][-1]
        for c in range(1, len(grid[0]) - 1):
            # left -> right pass
            update_visibility_and_scores(LEFT, r, c)

            # right -> left pass
            update_visibility_and_scores(RIGHT, r, len(grid[0]) - c - 1)

    # go through columns in both direction
    for c in range(1, len(grid[0]) - 1):
        last_visible_height[TOP] = grid[0][c]
        last_visible_height[BOTTOM] = grid[-1][c]
        for r in range(1, len(grid) - 1):
            # top -> bottom pass
            update_visibility_and_scores(TOP, r, c)

            # bottom -> top pass
            update_visibility_and_scores(BOTTOM, len(grid) - r - 1, c)

    # sum visible trees
    part_one_result = sum((1 for v in chain.from_iterable(visibility) if any(v.values())))

    # get max score
    part_two_result = max((reduce(lambda a, b: a * b, s.values()) for s in chain.from_iterable(scores)))
    print(f'part one: {part_one_result}')
    print(f'part two: {part_two_result}')


main()
