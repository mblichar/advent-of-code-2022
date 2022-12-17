import sys
import re
import itertools


class ValveData:
    def __init__(self, rate, connected_valves, paths_to_other_valves):
        self.rate = rate
        self.connected_valves = connected_valves
        self.paths_to_other_valves = paths_to_other_valves


def parse_input():
    graph = dict()

    for line in sys.stdin.readlines():
        re_search = re.search('Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)', line)
        valve, rate, connected_valves = re_search.groups()
        graph[valve] = ValveData(int(rate), connected_valves.split(', '), None)

    return graph


def collect_path(came_from, end_valve):
    path = [end_valve]
    valve = end_valve
    while valve in came_from:
        valve = came_from[valve]
        path.append(valve)

    path.reverse()
    return path


def find_paths_to_valves(graph, start, valves_to_visit):
    valves_paths = []
    visited_valves = set()

    came_from = dict()
    queue = graph[start].connected_valves.copy()  # start with connected valves to not put "start" on a path
    while len(queue) > 0 and len(valves_to_visit) != 0:
        valve = queue.pop(0)
        visited_valves.add(valve)

        if valve in valves_to_visit:
            valves_paths.append(collect_path(came_from, valve))
            valves_to_visit = valves_to_visit - {valve}

        for v in graph[valve].connected_valves:
            if v not in visited_valves:
                came_from[v] = valve
                queue.append(v)

    return valves_paths


def max_pressure_for_valves(graph, valves_to_open, time):
    cases = [(['AA'], time, 0, valves_to_open)]

    max_pressure = 0
    max_pressure_path = None
    while len(cases) > 0:
        path, remaining_time, released_pressure, valves_to_open = cases.pop(0)
        current_valve = path[-1]

        if released_pressure > max_pressure:
            max_pressure = released_pressure
            max_pressure_path = path

        if remaining_time - 1 == 0 or len(valves_to_open) == 0:
            continue

        # open valve
        if current_valve in valves_to_open:
            remaining_time -= 1
            released_pressure += graph[current_valve].rate * remaining_time

        for path_to_valve in graph[current_valve].paths_to_other_valves:
            other_valve = path_to_valve[-1]
            if other_valve in valves_to_open and len(path_to_valve) + 1 < remaining_time:
                cases.append((path + path_to_valve, remaining_time - len(path_to_valve), released_pressure,
                              valves_to_open - {current_valve}))

        if released_pressure > max_pressure:
            max_pressure = released_pressure
            max_pressure_path = path

    return max_pressure, max_pressure_path


def part_one():
    graph = parse_input()
    valves_to_open = set(filter(lambda v: graph[v].rate > 0, graph.keys()))
    for valve, valve_data in graph.items():
        valve_data.paths_to_other_valves = find_paths_to_valves(graph, valve, valves_to_open - {valve})

    max_pressure, max_pressure_path = max_pressure_for_valves(graph, valves_to_open, 30)

    print('result:', max_pressure, max_pressure_path)


def generate_valves_splits(valves_to_open):
    return map(
        lambda c: (set(c), valves_to_open - set(c)),
        itertools.chain.from_iterable(
            itertools.combinations(valves_to_open, x) for x in range(len(valves_to_open) + 1)))


def part_two():
    graph = parse_input()
    valves_to_open = set(filter(lambda v: graph[v].rate > 0, graph.keys()))
    for valve, valve_data in graph.items():
        valve_data.paths_to_other_valves = find_paths_to_valves(graph, valve, valves_to_open - {valve})

    max_pressure, max_pressure_paths = 0, None
    for x in generate_valves_splits(valves_to_open):
        set_a, set_b = x
        a_pressure, a_path = max_pressure_for_valves(graph, set_a, 26)
        b_pressure, b_path = max_pressure_for_valves(graph, set_b, 26)

        if a_pressure + b_pressure > max_pressure:
            max_pressure = a_pressure + b_pressure
            max_pressure_paths = (a_path, b_path)
            print(set_a, set_b, max_pressure)

    print('result:', max_pressure, max_pressure_paths)


part_two() if sys.argv[1] == '2' else part_one()
