import sys
from collections import namedtuple


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.files = []
        self.sub_dirs = []
        self.size = 0
        self.parent = parent


File = namedtuple('File', ['name', 'size'])


def find_sub_directory(directory, sub_dir_name):
    return next((d for d in directory.sub_dirs if d.name == sub_dir_name), None)


def add_sub_directory(directory, sub_dir_name):
    sub_directory = Directory(sub_dir_name, directory)
    directory.sub_dirs.append(sub_directory)
    return sub_directory


def build_tree(lines):
    root = Directory('')

    current_directory = root
    for line in lines[1:]:
        tokens = line.rstrip('\n').split(' ')

        if tokens[0] == '$':
            if tokens[1] == 'cd':
                if tokens[2] == '..':
                    current_directory = current_directory.parent
                else:
                    dir_name = tokens[2]

                    directory = find_sub_directory(current_directory, dir_name)
                    if directory is not None:
                        current_directory = directory
                    else:
                        print('here', dir_name)
                        directory = add_sub_directory(current_directory, dir_name)
                        current_directory = directory
        else:
            # inside ls output
            size_or_dir, name = tokens

            if size_or_dir == 'dir':
                directory = find_sub_directory(current_directory, name)
                if directory is None:
                    add_sub_directory(current_directory, name)
            else:
                current_directory.files.append(File(name, int(size_or_dir)))

    return root


def main():
    lines = sys.stdin.readlines()

    root = build_tree(lines)
    part_one_result = 0
    dir_sizes = dict()

    # calculate sizes and result
    def calculate_dir_size(directory):
        directory.size = sum(f.size for f in directory.files) + sum(calculate_dir_size(d) for d in directory.sub_dirs)

        nonlocal part_one_result
        if directory.size <= 100000:
            part_one_result += directory.size

        dir_sizes[directory.name] = directory.size
        return directory.size

    calculate_dir_size(root)
    print(f'part 1: {part_one_result}')

    total = 70000000
    space_needed = 30000000
    free_space = total - root.size

    space_to_delete = space_needed - free_space
    size_to_delete = next((v for _, v in sorted(dir_sizes.items(), key=lambda x: x[1]) if v >= space_to_delete))
    print(f'part 2: {size_to_delete}')


main()
