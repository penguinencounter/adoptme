#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import typing

from pet_record import PetRecord


def find_id(
    animal_id: int,
    database: typing.List[PetRecord]
) -> typing.List[PetRecord]:
    """

    :param animal_id:
    :param database:
    :return:
    """
    results = [p for p in database if p.animal_id == animal_id]
    return results