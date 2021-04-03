import pet_database
import time
from pet_record import PetRecord

records = pet_database.load_pet_records("../data/pets.pkl")

rn = 0
for i in records:
    rn += 1
#   print("\b"*100,flush=True,end="")
#   print(f"record {rn}... ", end="")
    i.register_suitability_constraints()
#   time.sleep(0.01)
#rint(PetRecord.ALL_SUITABILITY_CONSTRAINTS)

#rint('\n\n\n')

print(PetRecord.csv_headers())
for i in records:
    i.clean_data()
    print(i.csv_data())

