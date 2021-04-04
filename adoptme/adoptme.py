#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import argparse
import datetime
import logging
import os

import typing

import pet_database
import pet_record
import scrape


def parse_command_line() -> argparse.Namespace:
    """Get command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pet_database',
        type=str,
        help='path to pet database'
    )
    parser.add_argument(
        '--image_dir',
        default='data/images'
    )
    parser.add_argument(
        '--log',
        default=None,
        help='log file path'
    )

    args = parser.parse_args()
    args.pet_database = os.path.abspath(os.path.expanduser(args.pet_database))
    args.image_dir = os.path.abspath(os.path.expanduser(args.image_dir))
    args.log = os.path.abspath(os.path.expanduser(args.log)) if args.log else None
    return args


def find_returned_pets(
    existing_pets: typing.List[int],
    all_pets: typing.List[pet_record.PetRecord]
) -> typing.List[int]:
    """

    :param existing_pets:
    :param all_pets:
    :return:
    """
    returned = []
    for e in existing_pets:
        all_instances_of_e = (p for p in all_pets if p.animal_id == e)
        for pet in all_instances_of_e:
            if not pet.departure:
                # Animal already in system as not adopted.
                break
        else:
            # Animal has been returned. :-(
            returned.append(e)

    return returned


def already_departed(
    pet_id: int,
    all_pets: typing.List[pet_record.PetRecord]
) -> bool:
    """Has pet already departed?

    :param pet_id:
    :param all_pets:
    :return:
    """
    all_instances_of_pet_id = (p for p in all_pets if p.animal_id == pet_id)
    for pet in all_instances_of_pet_id:
        if not pet.departure:
            # At least one departure not populated. Pet has not departed.
            result = False
            break
    else:
        # All departures are populated. Pet has already departed.
        result = True

    return result


def classify_pets(
    current_pets: typing.List[int],
    all_pets: typing.List[pet_record.PetRecord],
    photos_path: str
) -> typing.Tuple[
    typing.List[int],
    typing.List[int],
    typing.List[int],
    typing.List[int]
]:
    """Classify current pets as new or existing.

    :param current_pets:
    :param all_pets:
    :param photos_path:
    :return: new, existing
    """
    existing = []
    new = []
    photoless = []
    all_pet_ids = set((p.animal_id for p in all_pets))
    for pet_id in current_pets:
        if pet_id in all_pet_ids:
            existing.append(pet_id)
            if not os.path.exists(os.path.join(photos_path, f'{pet_id}.jpg')):
                photoless.append(pet_id)
        else:
            new.append(pet_id)

    adopted = [
        pet_id
        for pet_id in all_pet_ids
        if pet_id not in current_pets and not already_departed(pet_id, all_pets)
    ]
    returned = find_returned_pets(existing, all_pets)

    return new, returned, adopted, photoless


def update_adopted_pets(
    all_pets: typing.List[pet_record.PetRecord],
    adopted_pets: typing.List[int],
    today: datetime.date
) -> None:
    """Set departure time for adopted pets.

    :param all_pets:
    :param adopted_pets:
    :param today:
    :return:
    """
    for adopted in adopted_pets:
        all_instances_of_adopted = (p for p in all_pets if p.animal_id == adopted)
        for pet in all_instances_of_adopted:
            if not pet.departure:
                pet.departure = today
                break
        else:
            logging.warning(
                f'All records for pet ID {adopted} had departure dates.'
            )


def add_pet_images(
    pets_sans_photos: typing.List[int],
    url: str,
    img_url: str,
    image_path: str,
    returned: bool
) -> typing.List[pet_record.PetRecord]:
    """Add missing pet photos to database.

    :param pets_sans_photos:
    :param url:
    :param img_url:
    :param image_path:
    :param returned:
    :return:
    """
    pet_info = (scrape.get_animal(url.format(p), returned) for p in pets_sans_photos)
    try:
        pets, img_uris = zip(*pet_info)
        for animal_id, img_uri in zip(pets_sans_photos, img_uris):
            if img_uri:
                dest = os.path.join(image_path, f'{animal_id}.jpg')
                photo_url = img_url + img_uri
                scrape.get_photo(dest, photo_url)

    except ValueError:
        pets = []

    return pets


def add_pets(
    all_pets: typing.List[pet_record.PetRecord],
    new_pets: typing.List[int],
    url: str,
    img_url: str,
    img_path: str,
    returned: bool = False
) -> None:
    """Add new pets to database.

    :param all_pets:
    :param new_pets:
    :param url:
    :param img_url:
    :param img_path:
    :param returned:
    :return:
    """
    pets = add_pet_images(new_pets, url, img_url, img_path, returned)
    all_pets += list(pets)


def main():
    """Scrape data from the interwebs."""
    args = parse_command_line()
    today = datetime.date.today()
    base_url = 'https://tje3xq7eu2.execute-api.us-west-1.amazonaws.com/production/'
    current_pets_url = base_url + 'search?AnimalType=Dog&AnimalType=Puppy&Location=ALL&StatusCategory=available'
    animal_url = base_url + 'animal?Id={}'
    img_url = 'https://do31x39459kz9.cloudfront.net'

    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
    now = datetime.datetime.now().isoformat(sep=' ', timespec='minutes')
    now_old = datetime.datetime.now()

    try:
        if not os.path.exists(args.image_dir):
            os.makedirs(args.image_dir)
        logging.info(f"Loading pet records.")
        all_pets = pet_database.load_pet_records(args.pet_database)
        logging.info(f"Fetching current pets.")
        current_pets = scrape.get_available_pets(current_pets_url)
        logging.info(f"Classifying pets.")
        new_pets, returned_pets, adopted_pets, photoless_pets = classify_pets(
            current_pets,
            all_pets,
            args.image_dir
        )
        logging.info(f"{new_pets} new, {returned_pets} returned, {adopted_pets} adopted, {photoless_pets} photoless")
        logging.info(f"Updating adoption time data.")
        update_adopted_pets(all_pets, adopted_pets, today)
        logging.info(f"Adding new records and photos.")
        add_pets(
            all_pets,
            new_pets,
            animal_url,
            img_url,
            args.image_dir
        )
        add_pets(
            all_pets,
            returned_pets,
            animal_url,
            img_url,
            args.image_dir,
            returned=True
        )
        logging.info(f"Saving...")
        pet_database.save_pet_records(
            all_pets,
            args.pet_database
        )
        logging.info(f"Saved.")
        logging.info(f"Trying to get images for pets without them.")
        add_pet_images(
            photoless_pets,
            animal_url,
            img_url,
            args.image_dir,
            returned=False
        )
    #     Format time.
        now_new = datetime.datetime.now()
        delta = now_new - now_old
        seconds = delta.total_seconds()
    except Exception as e:
        logging.error(f'Error updating database on {now_old}: {e}')
    else:
        logging.info(f'Database updated on {now}, took {seconds}s')
        logging.info(f'   {len(new_pets)} pets added. {new_pets}')
        logging.info(f'   {len(adopted_pets)} pets adopted. {adopted_pets}')
        logging.info(f'   {len(returned_pets)} pets returned. {returned_pets}')
        logging.info(f'   {len(all_pets)} records in database.')


if __name__ == '__main__':
    main()
