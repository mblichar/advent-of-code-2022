import sys
import re
import operator

ORE_IDX = 0
CLAY_IDX = 1
OBSIDIAN_IDX = 2
GEODE_IDX = 3


def add_tuples(a, b):
    return tuple(map(operator.add, a, b))


def sub_tuples(a, b):
    return tuple(map(operator.sub, a, b))


def parse_input():
    blueprints = []
    for line in sys.stdin.readlines():
        result = map(lambda x: int(x), re.search(
            'Blueprint .+: Each ore robot costs (.+) ore. Each clay robot costs (.+) ore. Each obsidian robot costs (.+) ore and (.+) clay. Each geode robot costs (.+) ore and (.+) obsidian.',
            line).groups())
        blueprints.append(((next(result), 0, 0, 0), (next(result), 0, 0, 0), (next(result), next(result), 0, 0),
                           (next(result), 0, next(result), 0)))

    return blueprints


def max_geodes(blueprint, robots, resources, remaining_time, cache):
    if remaining_time == 0:
        return resources[GEODE_IDX]

    cache_key = remaining_time
    if cache_key in cache['time_geodes']:
        if cache['time_geodes'][cache_key] > resources[GEODE_IDX]:
            return resources[GEODE_IDX]
    cache['time_geodes'][cache_key] = resources[GEODE_IDX]

    cache_key = (tuple(robots), resources)
    if cache_key in cache['state_time']:
        if cache['state_time'][cache_key] > remaining_time:
            return resources[GEODE_IDX]
    cache['state_time'][cache_key] = remaining_time

    can_build_robot = [False, False, False, False]
    for idx, cost in enumerate(blueprint['costs']):
        can_build = True
        for r, c in zip(resources, cost):
            if c > r:
                can_build = False
                break

        can_build_robot[idx] = can_build

    max_result = resources[GEODE_IDX]
    resources = add_tuples(resources, tuple(robots))
    if can_build_robot[GEODE_IDX]:
        new_robots = robots.copy()
        new_robots[GEODE_IDX] += 1
        new_resources = sub_tuples(resources, blueprint['costs'][GEODE_IDX])
        return max_geodes(blueprint, new_robots, new_resources, remaining_time - 1, cache)

    for idx, can_build in enumerate(can_build_robot[:-1]):
        if not can_build or robots[idx] >= blueprint['max_needed'][idx]:
            continue

        new_robots = robots.copy()
        new_robots[idx] += 1
        new_resources = sub_tuples(resources, blueprint['costs'][idx])
        max_result = max(max_result, max_geodes(blueprint, new_robots, new_resources, remaining_time - 1, cache))

    return max(max_result, max_geodes(blueprint, robots, resources, remaining_time - 1, cache))


def part_one():
    blueprints = parse_input()
    result = 0
    for idx, blueprint in enumerate(blueprints, 1):
        blueprint_data = {
            'costs': blueprint,
            'max_needed': [max(map(lambda cost: cost[idx], blueprint)) for idx in range(len(blueprint[0]))]
        }
        max_ = max_geodes(blueprint_data, [1, 0, 0, 0], (0, 0, 0, 0), 24, {'time_geodes': dict(), 'state_time': dict()})
        print(idx, max_)
        result += idx * max_

    print('result:', result)


def part_two():
    blueprints = parse_input()
    result = 0
    for idx, blueprint in enumerate(blueprints[:3], 1):
        blueprint_data = {
            'costs': blueprint,
            'max_needed': [max(map(lambda cost: cost[idx], blueprint)) for idx in range(len(blueprint[0]))]
        }
        max_ = max_geodes(blueprint_data, [1, 0, 0, 0], (0, 0, 0, 0), 32, {'time_geodes': dict(), 'state_time': dict()})
        print(idx, max_)
        result *= max_

    print('result:', result)


part_one() if sys.argv[1] == '1' else part_two()
