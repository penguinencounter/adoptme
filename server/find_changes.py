import csv
import os
import sys

import typing


def compare(x: list, y: list) -> typing.Tuple[list, list]:
    x_and_not_y = []
    y_and_not_x = []
    for line in x:
        if line not in y:
            x_and_not_y.append(line)

    for line in y:
        if line not in x:
            y_and_not_x.append(line)

    return x_and_not_y, y_and_not_x


def main(arg=None, path=None):
    try:
        if not (arg and path):
            arg = sys.argv[1]
            path = sys.argv[2]
        else:
            arg = arg
            path = path
    except KeyError:
        print("-!- Not enough arguments! -!-")
        print("USAGE: find_changes.py (help|start|finish) data_path")
        print("---")
        print("help: Show this help screen")
        print("start: Make a copy before scraping")
        print("finish: Find and report changes")
        return
    if arg in ['-h', '--help', 'help']:
        print("USAGE: find_changes.py (help|start|finish) data_path")
        print("---")
        print("help: Show this help screen")
        print("start: Make a copy before scraping")
        print("finish: Find and report changes")
        return
    elif arg == 'start':
        with open(path, 'r') as f:
            with open(f'/home/pi/server/temp_{path.split("/")[-1]}', 'w') as wf:
                wf.write(f.read())

        print("[START] command finished")
    elif arg == 'finish':
        if os.path.exists(f'/home/pi/server/temp_{path.split("/")[-1]}'):
            data = [[], []]
            with open(f'/home/pi/server/temp_{path.split("/")[-1]}', 'r') as f:
                data[0] = f.read().split('\n')
            with open(path, 'r') as f:
                data[1] = f.read().split('\n')
            old_rows = []
            new_rows = []
            old_itr = csv.reader(data[0])
            for row in old_itr:
                old_rows.append(row)
            new_itr = csv.reader(data[1])
            for row in new_itr:
                new_rows.append(row)

            removed, added = compare(old_rows, new_rows)
            print(f"{len(removed)} removed, {len(added)} added")
            print("[FINISH] command finished")
            with open("/home/pi/server/changelog.txt", 'w') as f:
                f.write(f"Database changes: {len(added)} dogs were added, and {len(removed)} were removed.\nId: [Name, Sex, Breed1, Breed2, CrossBreed?, AgeYears, AgeMonths, AgeApproximate?, Location, Date Added, Date Removed]\n\nAdded:\n")
                for item in added:
                    f.write(f"{item[0]}: {item[1:]}\n")
                f.write("\nRemoved:\n")
                for item in removed:
                    f.write(f"{item[0]}: {item[1:]}\n")


if __name__ == '__main__':
    main()
