#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import argparse
import cmd
import os

import typing

import pet_database
from pet_record import PetRecord


class InspectPets(cmd.Cmd):
    """Command Loop."""
    def __init__(self, records: typing.List[PetRecord]):
        """Constructor."""
        super(InspectPets, self).__init__()
        self.records = records
        self.prompt = 'Pets>> '

    def do_any_breed(self, arg: str):
        """Find pets by either breed."""
        arg = arg.lower()
        res = [
            r
            for r in self.records
            if (
                arg in r.breed_primary.name.lower() or
                (
                    r.breed_secondary and
                    arg in r.breed_secondary.name.lower()
                )
            )
        ]
        print_results(res)

    def do_breed(self, arg: str):
        """Find pets by primary breed."""
        res = [
            r
            for r in self.records
            if arg.lower() in r.breed_primary.name.lower()
        ]
        print_results(res)

    def do_color(self, arg: str):
        """Find pets by color."""
        res = [r for r in self.records if arg.lower() == r.color_code.name]
        print_results(res)

    def do_id(self, arg: str):
        """Find pets by ID."""
        arg = int(arg)
        res = [r for r in self.records if arg == r.animal_id]
        print_results(res)

    def do_name(self, arg: str):
        """Find pets by name."""
        res = [r for r in self.records if arg.lower() in r.name.lower()]
        print_results(res)

    def do_returned(self, _):
        """Find pets with `repeat_engagement` flag set."""
        res = [r for r in self.records if r.repeat_engagement]
        print_results(res)

    def do_secondary_breed(self, arg: str):
        """Find pets by secondary breed."""
        res = [
            r
            for r in self.records
            if (
                r.breed_secondary and
                arg.lower() in r.breed_secondary.name.lower()
            )
        ]
        print_results(res)

    @staticmethod
    def do_q(_):
        """Exit."""
        return True


def print_results(res: typing.List[PetRecord]):
    """Display results."""
    if not res:
        print('Not found.')
    else:
        print(f'{len(res)} records found.\n')
        for r in res:
            print(r)


def parse_command_line() -> argparse.Namespace:
    """Parse command line arguments.

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('database', help='Path to pet database.')

    args = parser.parse_args()
    args.database = os.path.abspath(os.path.expanduser(args.database))

    return args


def main() -> None:
    """

    :return:
    """
    args = parse_command_line()
    records = pet_database.load_pet_records(args.database)
    InspectPets(records).cmdloop()


if __name__ == '__main__':
    main()
