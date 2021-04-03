#
# Copyright 2019 Andrew Lin. All rights reserved.
#
# This software is released under the BSD 3-clause license. See LICENSE.txt or
# https://opensource.org/licenses/BSD-3-Clause for more information.
#
import datetime
import logging
import re
import typing


class NameId(typing.NamedTuple):
    """Name, Identifier pair."""
    # Human-meaningful identifier.
    name: str
    # Machine-friendly equivalent.
    identifier: int


def NullID():
    return NameId("NULL","NULL")


class PetRecord:
    ALL_SUITABILITY_CONSTRAINTS = []
    """Pet Record."""
    def __init__(self):
        """Construct empty PetRecord."""
        # Animal information from external provider.
        self.age_group: typing.Optional[NameId] = None
        self.animal_id: typing.Optional[int] = None
        self.breed_primary: typing.Optional[NameId] = None
        self.breed_secondary: typing.Optional[NameId] = None
        self.color_code: typing.Optional[NameId] = None
        self.date_of_birth: typing.Optional[datetime.date] = None
        self.gender: typing.Optional[NameId] = None
        self.intake_date: typing.Optional[datetime.date] = None
        self.location: typing.Optional[NameId] = None
        self.name: typing.Optional[str] = None
        self.source: typing.Optional[NameId] = None
        self.suitability_constraints: typing.Optional[typing.List[NameId]] = None
        self.surrender_reason: typing.Optional[NameId] = None

        # Additional information. Leading underscore variables are accessed via
        # properties.
        self._departure: typing.Optional[datetime.date] = None
        self._adoption_time: typing.Optional[datetime.timedelta] = None
        self.repeat_engagement: bool = False

    def __str__(self) -> str:
        """Pet Record as string."""
        s = (
            f'PetRecord:\n'
            f'   animal_id..............: {self.animal_id}\n'
            f'   name...................: {self.name}\n'
            f'   breed_primary..........: {self.breed_primary}\n'
            f'   breed_secondary........: {self.breed_secondary}\n'
            f'   age_group..............: {self.age_group}\n'
            f'   date_of_birth..........: {self.date_of_birth}\n'
            f'   gender.................: {self.gender}\n'
            f'   location...............: {self.location}\n'
            f'   source.................: {self.source}\n'
            f'   surrender_reason.......: {self.surrender_reason}\n'
            f'   color_code.............: {self.color_code}\n'
            f'   suitability_constraints: {self.suitability_constraints}\n'
            f'   intake_date............: {self.intake_date}\n'
            f'   departure..............: {self.departure}\n'
            f'   adoption_time..........: {self.adoption_time}\n'
            f'   repeat_engagement......: {self.repeat_engagement}\n'
        )

        return s
    
    @classmethod
    def csv_headers(cls):
        """
        Create CSV Headers
        """
        strbuild = '"animal_id","name","breed_primary","breed_primary_id","breed_secondary","breed_secondary_id","age_group","age_group_id",' \
               '"date_of_birth","gender","gender_id","location","location_id","source","source_id","surrender_reason","surrender_reason_id",' \
               '"color_code","color_code_id",'
        for const in cls.ALL_SUITABILITY_CONSTRAINTS:
            strbuild += f'"{const.name}",'
        postSection = '"intake_date","departure","adoption_time","return"'
        strbuild += postSection
        return strbuild
    
    def clean_data(self):
#       print(f"[{self.animal_id}] data clean... ", end="", flush=True)
        if self.name is None:
#           print("name, ", end="", flush=True)
            self.name = "NULL"
        if self.breed_primary is None:
#           print("pbreed, ", end="", flush=True)
            self.breed_primary = NullID()
        if self.breed_secondary is None:
#           print("sbreed, ", end="", flush=True)
            self.breed_secondary = NullID()
        if self.age_group is None:
#           print("agegrp, ", end="", flush=True)
            self.age_group = NullID()
        if self.date_of_birth is None:
#           print("dob, ", end="", flush=True)
            self.date_of_birth = "NULL"
        if self.gender is None:
#           print("gender, ", end="", flush=True)
            self.gender = NullID()
        if self.location is None:
#           print("loc, ", end="", flush=True)
            self.location = NullID()
        if self.source is None:
#           print("src, ", end="", flush=True)
            self.source = NullID()
        if self.surrender_reason is None:
#           print("surres, ", end="", flush=True)
            self.surrender_reason = NullID()
        if self.color_code is None:
#           print("col, ", end="", flush=True)
            self.color_code = NullID()
        if self.suitability_constraints is None:
#           print("sc, ", end="", flush=True)
            self.suitability_constraints = []
        if self.intake_date is None:
#           print("intake_dt, ", end="", flush=True)
            self.intake_date = "NULL"
        if self.departure is None:
#           print("dep_dt, ", end="", flush=True)
            self.departure = "NULL"
        if self._adoption_time is None:
#           print("adopt_diff, ", end="", flush=True)
            self.adoption_time_out = "\"NULL\""
        else:
            self.adoption_time_out = str(self.adoption_time.days)
        if self.repeat_engagement is None:
#           print("return, ", end="", flush=True)
            self.repeat_engagement = "NULL"
#       print()
 
    def csv_data(self):
        pre_const = f'{self.animal_id},"{self.name}","{self.breed_primary.name}",{self.breed_primary.identifier},"{self.breed_secondary.name}",{self.breed_secondary.identifier},"{self.age_group.name}",{self.age_group.identifier},"{str(self.date_of_birth)}","{self.gender.name}",{self.gender.identifier},"{self.location.name}",{self.location.identifier},"{self.source.name}",{self.source.identifier},"{self.surrender_reason.name}",{self.surrender_reason.identifier},"{self.color_code.name}",{self.color_code.identifier},'
        for const in PetRecord.ALL_SUITABILITY_CONSTRAINTS:
            if const in self.suitability_constraints:
                pre_const += '1,'
            else:
                pre_const += '0,'
        post_const = f'"{str(self.intake_date)}","{str(self.departure)}",{str(self.adoption_time_out)},'
        if self.repeat_engagement:
            post_const += '1'
        else:
            post_const += '0'
        return pre_const + post_const
    
    def register_suitability_constraints(self):
        for const in self.suitability_constraints:
            if const not in PetRecord.ALL_SUITABILITY_CONSTRAINTS:
                PetRecord.ALL_SUITABILITY_CONSTRAINTS.append(const)
        #       print(f"registered... {len(PetRecord.ALL_SUITABILITY_CONSTRAINTS)} so far",end="")

    @classmethod
    def from_animal_record(cls, record: dict):
        """Create PetRecord from animal scrape.

        :param record:
        :return:
        """
        pet = cls()
        r = record.get('Age', {}).get('AgeGroup')
        pet.age_group = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        pet.animal_id = record.get('Id')
        r = record.get('Breed', {}).get('Primary')
        pet.breed_primary = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        r = record.get('Breed', {}).get('Secondary')
        pet.breed_secondary = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        pet.color_code = extract_color_code(record.get('AdoptionSummary'))
        pet.date_of_birth = extract_date_from_iso_time(
            record.get('DateOfBirthUtc')
        )
        r = record.get('Sex')
        pet.gender = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        pet.intake_date = extract_date_from_iso_time(
            record.get('Intake', {}).get('DateUtc')
        )
        r = record.get('Location', {}).get('PhysicalLocation')
        pet.location = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        pet.name = record.get('Name')
        r = record.get('Intake', {}).get('Source')
        pet.source = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )
        r = record.get('Icons')
        pet.suitability_constraints = (
            sorted(
                (
                    NameId(constraint.get('Name'), constraint.get('Id'))
                    for constraint in r
                ),
                key=lambda x: x.identifier
            )
            if r else
            []
        )
        r = record.get('Intake', {}).get('SurrenderReason')
        pet.surrender_reason = (
            NameId(r.get('Name'), r.get('Id'))
            if r else
            None
        )

        return pet

    @property
    def departure(self):
        """Departure (adoption) date of pet."""
        return self._departure

    @departure.setter
    def departure(self, when: datetime.date):
        """Set departure date for PetRecord.

        :param when:
        :return:
        """
        if self._departure:
            logging.warning(
                f'Overwriting departure date of {self._departure.isoformat()} '
                f'for pet {self.animal_id} with {when.isoformat()}'
            )

        self._departure = when
        if self.intake_date and self.intake_date != "NULL" and self._departure != "NULL":
            self._adoption_time = self._departure - self.intake_date

    @property
    def adoption_time(self):
        """Number of days for pet to get adopted."""
        return self._adoption_time


def extract_color_code(
    summary: str
) -> NameId:
    """Extract color code from animal summary.

    '... My Personality Color Code is <b>COLOR</b>; ...'

    :param summary: Animal summary.
    :return: Color code from summary or empty string.
    """
    codes = [None, 'blue', 'orange', 'purple']
    res = re.search(
        r'My Personality Color Code is <b>(\w*)\W?</b>',
        summary
    )
    try:
        color = res.group(1).lower()
    except (AttributeError, IndexError):
        color = None

    color_id = codes.index(color)
    return NameId(color, color_id)


def extract_date_from_iso_time(t: str) -> typing.Optional[datetime.date]:
    """Get date record from date-time string.

    Assumed format: YYYY-MM-DDTHH:MM:SSZ

    :param t: ISO date-time string
    :return:
    """
    if not t:
        return None

    date, _ = t.split('T')
    return datetime.date.fromisoformat(date)
