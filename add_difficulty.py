import csv
import json
from pathlib import Path


from engine import Engine

BASEPATH = Path(__name__).parent  # permet l'utilisation sur tous les systeme


with open(BASEPATH / "difficulty_set.csv", "r", encoding="utf-8") as f:
    diff_data = list(csv.reader(f, delimiter=";"))

country_data = Engine.load_country_data(Engine())

print(diff_data[0][2])
print(diff_data[0])

for diff in diff_data:
    print(diff[2])

for item in country_data:
    for diff in diff_data:
        if item["code"] == diff[1]:
            item["difficulty"] = int(diff[2])

with open("countries.json", "w", encoding="utf-8") as f:
    json.dump(country_data, f, ensure_ascii=False, indent=4)
