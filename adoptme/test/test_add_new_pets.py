#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import datetime

from adoptme import add_new_pets
from pet_database import PetRecord


def test_add_empty_to_empty():
    """Add an empty list to an empty list."""
    all_pets = []
    current_pets = []
    add_new_pets(all_pets, current_pets, datetime.date.today(), False)
    assert len(all_pets) == 0


def test_add_to_empty():
    """Add pets to an empty all_pets."""
    today = datetime.date.today()
    all_pets = []
    current_pets = [
        PetRecord(
            1,
            'Fido',
            'Female',
            'Pug',
            '',
            False,
            2,
            3,
            True,
            'Testville'
        )
    ]
    add_new_pets(all_pets, current_pets, today, False)

    assert len(all_pets) == 1
    assert all_pets[0] == current_pets[0]
    assert all_pets[0].arrival == today


def test_initialize():
    """Add pets to an empty all_pets."""
    today = datetime.date.today()
    all_pets = []
    current_pets = [
        PetRecord(
            1,
            'Fido',
            'Female',
            'Pug',
            '',
            False,
            2,
            3,
            True,
            'Testville'
        )
    ]
    add_new_pets(all_pets, current_pets, today, True)

    assert len(all_pets) == 1
    assert all_pets[0] == current_pets[0]
    assert all_pets[0].arrival is None


def test_no_new_pets():
    """Add no new pets."""
    today = datetime.date.today()
    fido = PetRecord(
        1,
        'Fido',
        'Female',
        'Pug',
        '',
        False,
        2,
        3,
        True,
        'Testville'
    )
    all_pets = [fido]
    current_pets = [fido]
    add_new_pets(all_pets, current_pets, today, False)

    assert len(all_pets) == 1
    assert all_pets[0] == fido


def test_new_pets():
    """Add new pets."""
    today = datetime.date.today()
    lady = PetRecord(
        1,
        'Lady',
        'Female',
        'Cocker Spaniel',
        '',
        False,
        2,
        3,
        True,
        'Testville'
    )
    tramp = PetRecord(
        2,
        'Tramp',
        'Male',
        'Terrier',
        '',
        True,
        3,
        0,
        True,
        'Testville'
    )
    all_pets = [lady]
    current_pets = [lady, tramp]
    add_new_pets(all_pets, current_pets, today, False)

    assert len(all_pets) == 2
    assert all_pets[0] == lady
    assert all_pets[1] == tramp
