#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import datetime

from adoptme import update_adopted_pets
from pet_database import PetRecord


def test_empty_update():
    """"""
    today = datetime.date.today()
    all_pets = []
    current_pets = []

    update_adopted_pets(all_pets, current_pets, today)

    assert len(all_pets) == 0


def test_no_update():
    """"""
    today = datetime.date.today()
    spot = PetRecord(
        5,
        'Spot',
        'Female',
        'Shar pei',
        '',
        True,
        11,
        0,
        True,
        'Upland'
    )
    all_pets = [spot]
    current_pets = [spot]
    update_adopted_pets(all_pets, current_pets, today)

    assert len(all_pets) == 1
    assert spot.departure is None


def test_update():
    """"""
    today = datetime.date.today()
    see = PetRecord(
        3,
        'See',
        'Male',
        'Beagle',
        '',
        True,
        11,
        0,
        True,
        'Upland'
    )
    spot = PetRecord(
        4,
        'Spot',
        'Female',
        'Shar pei',
        '',
        True,
        10,
        0,
        True,
        'Upland'
    )
    run = PetRecord(
        5,
        'Run',
        'Male',
        'Shepherd',
        '',
        True,
        12,
        0,
        True,
        'Upland'
    )
    all_pets = [see, spot, run]
    current_pets = [see, run]
    update_adopted_pets(all_pets, current_pets, today)

    assert len(all_pets) == 3
    assert spot.departure == today
    assert see.departure is None
    assert run.departure is None
