import csv
import random

from pathlib import Path
import json
import pickle
import unicodedata #permet d'uniformiser les accents
from rapidfuzz import distance #permet de calculer la distance entre 2 mots

from kivy.app import App

from uikivy import GOALSCORE

"""
CONSTANTES
"""

#Fonctions utilitaires :

BASEPATH = Path(__name__).parent #permet l'utilisation sur tous les systeme

class Engine :
    def __init__(self):
        super().__init__()
        self.data_size = None
        self.iso = None
        self.country_data = None
        self.score = 0
        self.lives = 3


    @property
    def app(self):
        return App.get_running_app()


    def load_country_data(self, path = None) -> list[dict]:

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
                self.country_data = json.load(f)
        except FileNotFoundError:
            path = BASEPATH / "countries.json" #si pas de fichier trouvé, on force le fichier présent de base
            with open(path, 'r', encoding='utf-8') as f:
                country_data = json.load(f)
            raise FileNotFoundError("aucun fichier trouvé/utilisation du fichier par défaut")

        for item in self.country_data:
            if item["continents"].lower() == "north america" or item["continents"].lower() == "south america":
                item["continents"] = "America"

        self.country_data = self.manage_difficulty(self.country_data)



        ### Permet d'exporter la liste des pays et iso
        # liste_export = []
        # for item in country_data:
        #     #ligne = f"{item['name']};{item['code']}"
        #     liste_export.append((item["name"], item["code"]))
        #
        # with open("export.csv", "w", encoding="utf-8", newline="") as f:
        #     writer = csv.writer(f, delimiter=";")
        #     #writer.writerow(["name", "code"])
        #     for nom, iso in liste_export:
        #         writer.writerow([nom, iso])

        return self.country_data


    @staticmethod
    def manage_difficulty(country_data):
        #pour l'instant ne gère pas vraiment de choix de difficulté mais ne montre pas les difficiles
        difficulty_list = [1,2]
        filtered = []
        for item in country_data:
            if item["difficulty"] in difficulty_list:
                filtered.append(item)

        return filtered



    def load_iso(self, continent = 'Monde'):
        def __init__(self, **kwargs):
            ...
        #la fonction de jeu chargera tous les iso puis choisira un au hasard qui sera renseigné aux fonction sd'affichage
        data = self.load_country_data()
        ...

    def get_name(self, iso):
        data = self.app.engine.load_country_data()
        for item in data:
            if item["code"] == iso:
                return  item["name"]
        return None

    @staticmethod
    def get_flag(iso):
        return str(BASEPATH / "flags" / f"{iso}.png")

    def get_capitals(self, iso):
        data = self.app.engine.load_country_data()
        for item in data:
            if item["code"] == iso:
                return item["capital"]
        return None

    #Fonctions de jeu :

    def check_answer(self, type_quizz, iso, answer): #dispatcher de mode de jeu
        if type_quizz == 'Capitale':
            return self.app.engine.check_capital(iso, answer)
        elif type_quizz == 'Drapeau':
            self.app.engine.check_flags(iso, answer)
        elif type_quizz == 'Tout': #pas ici que le choix doit se faire, la logique de verification se fait as comme ca
            rand_value = random.randint(1,2)
            self.app.engine.check_capital(iso, answer) if rand_value == 1 else self.app.engine.check_flags(iso, answer)

    def check_capital(self, iso, answer):
        #affiche une question (sera bouclée dans une fonction de jeu plus générale qui choisira d'afficher question capitale, flag ou les deux)
        country_capital = self.app.engine.get_capitals(iso)
        if self.manage_answer(answer.lower(), country_capital.lower()):
        #if answer.lower() == country_capital.lower() :
            self.score += 1
            return True
        elif answer.lower() == 'debug':
            self.score += 1
            return True
        else :
            self.lives -=1
            return False

    def manage_answer(self, answer, data):  # gere la tolerance orthographique
        cleaned_answer = self.clean_text(answer)
        cleaned_data = self.clean_text(data)

        nb_error = distance.Levenshtein.distance(cleaned_answer, cleaned_data)

        if len(cleaned_data) < 5:
            if nb_error <= 2:
                return True
            else:
                return False #on accepte max 2 erreurs sur les mot de moins de 5 lettres
        else:
            if nb_error <= 3:
                return True
            else:
                return False




    @staticmethod
    def clean_text(text):
        text = text.strip().lower()  # retrait des espaces et mise en minuscule
        text = " ".join(
            c for c in unicodedata.normalize('NFD', text) #nfd (Normalization Form Canonical Decomposition) permet d'indiquer qu'on veut separer les accents de la lettre
            if unicodedata.category(c) != "Mn" # Mn (Mark, Nonspacing) permet d'indiquer qu'on ne veut pas garder les accents
        )
        return text


    def do_reset(self):
        self.score = 0
        self.lives = 3



    def check_flags(self, iso, answer):
        pass

    def get_filtered_countries(self, continent, all_data):
        if continent == "Monde":
            return all_data
        return [c for c in all_data if c["continents"] == continent]


    def save_score(self, pseudo, score, mode, type_quizz):
        ...#todo sauver pseudo, score et mode de jeu + type pour permettre d'afficher au bon endroit

    def load_score(self, mode, type_quizz):
        ... #todo ajouter tri des données pour donner les 10 meilleurs

    def create_game_data(self):
        all_data = self.load_country_data()
        data_quizz = self.get_filtered_countries(self.app.continent, all_data)
        self.data_size = len(data_quizz)
        print(f"taille {self.data_size}")
        random.shuffle(data_quizz)
        return data_quizz, self.data_size

    def is_endgame(self):
        print(f" data size : {self.data_size}")
        if self.app.mode == "mar" :
            #if len(self.app.question_ui.data_quizz) == 0:
            if self.data_size == 0:

                print(len(self.app.question_ui.data_quizz))
                print("fin is_endgame mar len = 0")
                return True

            elif self.app.engine.lives == 0:
                print("fin is_endgame mar lives = 0")
                return True
            else:
                return False

        elif self.app.mode == "norm":
            if self.app.engine.score == GOALSCORE:
                print("fin")
                return True

            elif self.data_size == 0:
                return True

            elif self.app.engine.lives == 0:
                print("fin")
                return True
            else:
                return False







