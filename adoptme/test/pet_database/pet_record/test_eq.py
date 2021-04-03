#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
from pet_database import PetRecord


def test_equality():
    """"""
    pet1 = PetRecord(
        1,
        'doggie',
        'Male',
        'Malamute',
        '',
        False,
        0,
        1,
        False,
        'Lap'
    )

    pet2 = PetRecord(
        2,
        'mcdogface',
        'Female',
        'Husky',
        '',
        False,
        0,
        1,
        False,
        'Lap'
    )

    assert pet1 == pet1
    assert pet1 != pet2


def test_in():
    """"""
    pet1 = PetRecord(
        1,
        'doggie',
        'Male',
        'Malamute',
        '',
        False,
        0,
        1,
        False,
        'Lap'
    )

    pet2 = PetRecord(
        2,
        'mcdogface',
        'Female',
        'Husky',
        '',
        False,
        0,
        1,
        False,
        'Lap'
    )

    pet3 = PetRecord(
        2,
        'fido',
        'Female',
        'Shepherd',
        '',
        False,
        0,
        1,
        False,
        'Lap'
    )

    kennel = [pet1, pet2]

    assert pet1 in kennel
    assert pet2 in kennel
    assert pet3 not in kennel
