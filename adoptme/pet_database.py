#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import pickle
import typing

from pet_record import PetRecord


def load_pet_records(path: str) -> typing.List[PetRecord]:
    """Load pet record database.

    :param path:
    :return:
    """
    try:
        with open(path, 'rb') as f:
            pets = pickle.load(f)
    except FileNotFoundError:
        pets = []

    return pets


def save_pet_records(pets: typing.List[PetRecord], path: str) -> None:
    """Save pet record database.

    :param pets:
    :param path:
    :return:
    """
    with open(path, 'wb') as f:
        pickle.dump(pets, f)
