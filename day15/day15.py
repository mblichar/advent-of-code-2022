import re
import sys
from collections import namedtuple

SensorData = namedtuple('SensorData', ('beacon', 'distance'))


def parse_input():
    sensors_data = dict()
    beacons = set()
    for line in sys.stdin.readlines():
        re_search = re.search('Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)', line)
        s_x, s_y, b_x, b_y = (int(x) for x in re_search.groups())
        sensors_data[(s_x, s_y)] = SensorData((b_x, b_y), abs(s_x - b_x) + abs(s_y - b_y))
        beacons.add((b_x, b_y))
    return sensors_data, beacons


def main():
    sensors_data, beacons = parse_input()
    is_part_one = sys.argv[1] == '1'
    if is_part_one:
        row_to_check = int(sys.argv[2])

        covered_points = set()
        for sensor, data in sensors_data.items():
            remaining_distance = data.distance - abs(sensor[1] - row_to_check)
            if remaining_distance >= 0:
                for i in range(-remaining_distance, remaining_distance + 1):
                    point = (sensor[0] + i, row_to_check)
                    if point not in beacons:
                        covered_points.add(point)

        print('result', len(covered_points))
    else:
        size_to_check = int(sys.argv[2]) + 1
        x, y = 0, 0
        while y < size_to_check:
            covered = False
            for sensor, data in sensors_data.items():
                if abs(x - sensor[0]) + abs(y - sensor[1]) <= data.distance:
                    covered = True
                    # skip fields covered by this sensor in given row
                    x = sensor[0] + (data.distance - abs(sensor[1] - y)) + 1
                    if x >= size_to_check:
                        x = 0
                        y += 1
                    break

            if not covered:
                print('result', x * 4000000 + y)
                break


main()
