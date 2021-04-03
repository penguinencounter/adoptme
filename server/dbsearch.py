import pet_database
from utilities.multi_if import case


def remove_duplicates(l: list):
    print(f"\nEntering new list... {l}\n")
    in_list = []
    for item in l:
        if item is None:
            print("'None' found in list. Still checking it, even though there might be a database problem...")
        if item not in in_list:
            in_list.append(item)
    return in_list


class DBSearch:
    keyword_basic = {"animal_id": 0,
                     "name": 1,
                     "breed": 2,
                     "age_group": 3,
                     "gender": 4,
                     "location": 5,
                     "source": 6,
                     "color_code": 7}

    def __init__(self, db_path):
        self.path = db_path
        self.db = pet_database.load_pet_records(self.path)
        self.possible_ids = {i.animal_id for i in self.db if i.animal_id is not None}
        self.possible_names = {i.name for i in self.db if i.name is not None}
        self.possible_breeds = {i.breed_primary.name for i in self.db if i.breed_primary is not None}
        self.possible_age_groups = {i.age_group.name for i in self.db if i.age_group is not None}
        self.possible_genders = {i.gender.name for i in self.db if i.gender is not None}
        self.possible_locations = {i.location.name for i in self.db if i.location is not None}
        self.possible_sources = {i.source.name for i in self.db if i.source is not None}
        self.possible_color_codes = {i.color_code.name for i in self.db if i.color_code is not None}

    def everything(self):
        return self.db

    def search(self, key: int, search):
        results = []

        def id_search(item, term):
            if term is not None:
                if item.animal_id is not None:
                    return item.animal_id == int(term)
                else:
                    return False
            else:
                return item.animal_id is None

        def name_search(item, term):
            if term is not None:
                if item.name is not None:
                    return term in item.name
                else:
                    return False
            else:
                return item.name is None

        def breed_search(item, term):
            if term is not None:
                if item.breed_primary is not None:
                    return term in item.breed_primary.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! breed is {item.breed} ... ", end="")
                return item.breed_primary is None or item.breed_primary.name is None

        def age_group_search(item, term):
            if term is not None:
                if item.age_group is not None:
                    return term in item.age_group.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! age_group is {item.age_group} ... ", end="")
                return item.age_group is None or item.age_group.name is None

        def gender_search(item, term):
            if term is not None:
                if item.gender is not None:
                    return term in item.gender.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! gender is {item.gender} ... ", end="")
                return item.gender is None or item.gender.name is None

        def location_search(item, term):
            if term is not None:
                if item.location is not None:
                    return term in item.location.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! location is {item.location} ... ", end="")
                return item.location is None or item.location.name is None

        def source_search(item, term):
            if term is not None:
                if item.source is not None:
                    return term in item.source.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! source is {item.source} ... ", end="")
                return item.source is None or item.source.name is None

        def color_code_search(item, term):
            if term is not None:
                if item.color_code is not None:
                    return term in item.color_code.name
                else:
                    return False
            else:
                print(f" HITTTTTT!!! color_code is {item.color_code} ... ", end="")
                return item.color_code is None or item.color_code.name is None

        for i in self.db:
            if i is not None:
                print(f"searching pet id #{i.animal_id} ... ", end="")
                add_bool = case(key,
                                [0, 1, 2, 3, 4, 5, 6, 7],
                                id_search,
                                name_search,
                                breed_search,
                                age_group_search,
                                gender_search,
                                location_search,
                                source_search,
                                color_code_search,
                                send=(i, search))
                if add_bool:
                    results.append(i)
        return results

