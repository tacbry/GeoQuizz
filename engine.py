from typing import List
from pathlib import Path
import json
import pickle

from kivy.storage.jsonstore import JsonStore

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


def load_iso(continent = 'Monde'):
    #la fonction de jeu chargera tous les iso puis choisira un au hasard qui sera renseigné aux fonction sd'affichage
    data = load_country_data()
    ...

def get_name(iso):
    data = load_country_data()
    for item in data:
        if item["code"] == iso:
            return  item["name"]
    return None


def get_flag(iso):
    return str(BASEPATH / "flags" / f"{iso}.png")

def get_capitals(iso):
    data = load_country_data()
    for item in data:
        if item["code"] == iso:
            return item["capital"]
    return None

def play_capitals(iso):
    #affiche une question (sera bouclée dans une fonction de jeu plus générale qui choisira d'afficher question capitale, flag ou les deux)
    print("QUIZZ CAPITALE")
    country_name = get_name(iso)
    country_flag = get_flag(iso) #pas utile pour le moment
    country_capital = get_capitals(iso)
    answer = ''

    while not answer.lower() == country_capital.lower():
        answer = input(f'Quelle est la capitale de ce pays : {country_name} ? ')
        if answer.lower() == country_capital.lower():
            print("Bonne réponse, +1 points")
        else:
            print("mauvaise réponse, réessayez")


