#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import argparse
import csv
import sys

import typing
from contextlib import contextmanager

from pet_record import PetRecord


def parse_command_line() -> argparse.Namespace:
    """Get command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_data', help='input file')
    parser.add_argument('-o', '--output', type=str, help='output file')
    args = parser.parse_args()

    return args


@contextmanager
def ostream(output: str):
    """Output stream."""
    if output:
        with open(output, 'w') as f:
            yield f

    else:
        yield sys.stdout


def process_data(f: typing.Iterable):
    """Generator to process pet data."""
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for idx, row in enumerate(reader):
        if idx == 0:
            continue

        pet = PetRecord.from_tuple(row)
        if pet.arrival and pet.departure:
            delta = pet.departure - pet.arrival
            yield (*pet.as_tuple()[:-2], delta.days)


def main():
    """Preprocess adoptme data."""
    args = parse_command_line()

    with open(args.raw_data) as fin, ostream(args.output) as fout:
        writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow((*PetRecord.headers()[:-2], 'days_to_adopt'))
        for p in process_data(fin):
            writer.writerow(p)


if __name__ == '__main__':
    main()
