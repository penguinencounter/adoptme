#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import logging
import shutil

import requests
import typing

import pet_record


def get_available_pets(url: str) -> typing.List[int]:
    """Get available pets at shelter."""
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f'Bad Result Code. {r.status_code}')

    j = r.json()
    records = j['response']
    pets = [record['AnimalId'] for record in records]

    return pets


def get_animal(
    url: str,
    returned: bool
) -> typing.Tuple[pet_record.PetRecord, str]:
    """Get animal info."""
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f'Bad Result Code. {r.status_code}')

    j = r.json()
    resp = j['response']
    pet = pet_record.PetRecord.from_animal_record(resp)
    if returned:
        pet.repeat_engagement = True

    photos = resp.get('Photos', [])
    photos = photos[0].get('Versions', []) if len(photos) else []
    img_uri = photos[0].get('1024') if len(photos) else None

    return pet, img_uri


def get_photo(dest: str, url: str) -> None:
    """Get animal photo.

    :param dest:
    :param url:
    :return:
    """
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        logging.warning('Unable to scrape {url}. Status code {r.status_code}.')
        return

    with open(dest, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
