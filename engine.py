from typing import List
from pathlib import Path
import json
import pickle

"""
CONSTANTES
"""
BASEPATH = Path(__name__).parent #permet l'utilisation sur tous les systeme

def load_country_data(path = None) -> list[dict]:

    if path is None:
        path = BASEPATH / "countries.json"
    else:
        path = path

    try:
        if path is None:
            path = BASEPATH / "countries.json"
        else:
            path = path

        with open(path, 'r', encoding='utf-8') as f:
            country_data = json.load(f)
    except FileNotFoundError:
        path = BASEPATH / "countries.json" #si pas de fichier trouvé, on force le fichier présent de base
        with open(path, 'r', encoding='utf-8') as f:
            country_data = json.load(f)
        raise FileNotFoundError("aucun fichier trouvé/utilisation du fichier par défaut")

    return country_data

# def get_country_data(path = None) -> dict:
#     data = load_country_data()
#     for item in data.items():
#         if item["name"] == "Albania":
#             print(item["capital"])


def get_name(iso):
    return str(BASEPATH / "name" / f"{iso}.png")

def get_flag(iso):
    return str(BASEPATH / "flags" / f"{iso}.png")

def get_capitals(iso):
    return str(BASEPATH / "capitals" / f"{iso}.csv")




