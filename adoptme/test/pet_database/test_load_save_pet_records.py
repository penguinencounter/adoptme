#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import tempfile

from pet_database import save_pet_records, load_pet_records, PetRecord


def test_empty_records():
    """Save and load database with no records."""
    with tempfile.NamedTemporaryFile() as f:
        save_pet_records([], f.name)
        pets = load_pet_records(f.name)

        assert len(pets) == 0


def test_single_record():
    """Save and load database with single record."""
    gold = PetRecord(
        42,
        'Maxwell',
        'male',
        'Corgi',
        'German Shepard',
        True,
        5,
        0,
        True,
        'San Diego',
        None,
        None
    )

    with tempfile.NamedTemporaryFile() as f:
        save_pet_records([gold], f.name)
        pets = load_pet_records(f.name)

        assert len(pets) == 1
        assert pets[0] == gold


def test_overwrite():
    """Overwrite the database file."""
    gold = PetRecord(
        42,
        'Maxwell',
        'male',
        'Corgi',
        'German Shepard',
        True,
        5,
        0,
        True,
        'San Diego',
        None,
        None
    )

    with tempfile.NamedTemporaryFile() as f:
        for _ in range(3):
            save_pet_records([gold], f.name)
            pets = load_pet_records(f.name)

            assert len(pets) == 1
            assert pets[0] == gold

