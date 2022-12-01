import sys


def main():
    lines = sys.stdin.readlines()
    line = lines[0]

    required_len = 4 if sys.argv[1] == "1" else 14

    for i in range(0, len(line) - required_len):
        if len(set(line[i:i+required_len])) == required_len:
            print(f"result: {i+required_len}")
            break


main()
