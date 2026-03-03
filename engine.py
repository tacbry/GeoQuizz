import random
from typing import List
from pathlib import Path
import json
import pickle

from kivy.storage.jsonstore import JsonStore

"""
CONSTANTES
"""

#Fonctions utilitaires :

BASEPATH = Path(__name__).parent #permet l'utilisation sur tous les systeme

class Engine :
    def __init__(self):
        super().__init__()
        self.iso = None


    def load_country_data(self,path = None) -> list[dict]:
        if path is None:
            path = BASEPATH / "countries.json"
        else:
            path = path

        try:
            if path is None:
                path = BASEPATH / "countries.json"
            else:
                path = path

            with path.open(encoding='utf-8') as f:
                country_data = json.load(f)

        except FileNotFoundError:
            path = BASEPATH / "countries.json" #si pas de fichier trouvé, on force le fichier présent de base
            with open(path, 'r', encoding='utf-8') as f:
                country_data = json.load(f)
            raise FileNotFoundError("aucun fichier trouvé/utilisation du fichier par défaut")

        for item in country_data:
            if item["continents"].lower() == "north america" or item["continents"].lower() == "south america":
                item["continents"] = "America"

        return country_data



    def get_name(self, iso):
        data = self.load_country_data()
        for item in data:
            if item["code"] == iso:
                return  item["name"]
        return None


    def get_flag_path(self, iso):
        return str(BASEPATH / "flags" / f"{iso}.png")

    def get_capitals(self, iso):
        data = self.load_country_data()
        for item in data:
            if item["code"] == iso:
                return item["capital"]
        return None

    #Fonctions de jeu :

    def play_game(self,type_quizz,iso, answer): #dispatcher de mode de jeu
        if type_quizz == 'Capitale':
            return self.play_capitals(iso, answer)
        elif type_quizz == 'Drapeau':
            self.play_flags(iso, answer)
        elif type_quizz == 'Tout':
            rand_value = random.randint(1,2)
            self.play_capitals(iso, answer) if rand_value == 1 else self.play_flags(iso, answer)
        return None

    def play_capitals(self, iso, answer):
        #affiche une question (sera bouclée dans une fonction de jeu plus générale qui choisira d'afficher question capitale, flag ou les deux)
        country_capital = self.get_capitals(iso)
        return True if answer.lower() == country_capital.lower() else False



    def play_flags(self, iso, answer):
        pass

    def get_filtered_countries(self, continent, all_data):
        if continent == "Monde":
            return all_data
        return [c for c in all_data if c["continents"] == continent]