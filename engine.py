import csv
import random

from pathlib import Path
import json
import unicodedata  # permet d'uniformiser les accents
from rapidfuzz import distance  # permet de calculer la distance entre 2 mots

from kivy.app import App

from uikivy import GOALSCORE

"""
CONSTANTES
"""

# Fonctions utilitaires :

BASEPATH = Path(__name__).parent  # permet l'utilisation sur tous les systeme


class Engine:
    """Core game engine handling data, logic, and scoring.

    Gère le chargement des données pays, la logique du quiz (capitales,
    drapeaux, mode mixte), la vérification des réponses, la gestion des vies,
    le score, la sélection des pays selon les filtres, ainsi que l'enregistrement
    et le tri des scores dans le leaderboard.

    Cette classe est indépendante de l'interface graphique et constitue
    le cœur fonctionnel du jeu.
    """

    def __init__(self):
        """
        Initialise l'instance du moteur de jeu.

        Prépare les variables de session : score, vies, données pays,
        paramètre du mode mixte et taille des données. Ne charge pas encore
        les données pays pour éviter les lectures inutiles.
        """
        super().__init__()
        self.data_size = None
        self.iso = None
        self.country_data = None
        self.score = 0
        self.lives = 3
        self.param_all = None  # pour gerer la correction du mode mixte

    @property
    def app(self):
        """
        Retourne l'instance de l'application Kivy en cours d'exécution.

        Permet au moteur d'accéder aux paramètres globaux (mode, continent,
        type de quiz, pseudo, etc.) définis dans l'application.
        """
        return App.get_running_app()

    def load_country_data(self, path=None) -> list[dict]:
        """
        Charge les données des pays depuis un fichier JSON.

        Paramètres
        ----------
        path : str ou Path, optionnel
            Chemin vers un fichier JSON personnalisé. Si None, utilise
            le fichier 'countries.json' par défaut.

        Retour
        ------
        list[dict]
            Liste de dictionnaires contenant les informations des pays.

        Exceptions
        ----------
        FileNotFoundError
            Si le fichier spécifié n'existe pas. Le moteur retombe alors
            sur le fichier par défaut et signale l'erreur.
        """
        if path is None:
            path = BASEPATH / "countries.json"
        else:
            path = path

        try:
            if path is None:
                path = BASEPATH / "countries.json"
            else:
                path = path

            with open(path, "r", encoding="utf-8") as f:
                self.country_data = json.load(f)
        except FileNotFoundError:
            path = (
                BASEPATH / "countries.json"
            )  # si pas de fichier trouvé, on force le fichier présent de base
            with open(path, "r", encoding="utf-8") as f:
                country_data = json.load(f)
            raise FileNotFoundError(
                "aucun fichier trouvé/utilisation du fichier par défaut"
            )

        for item in self.country_data:
            if (
                item["continents"].lower() == "north america"
                or item["continents"].lower() == "south america"
            ):
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
        """
        Filtre les pays selon leur niveau de difficulté.

        Paramètres
        ----------
        country_data : list[dict]
            Liste complète des pays chargés.

        Retour
        ------
        list[dict]
            Liste filtrée contenant uniquement les pays dont la difficulté
            est considérée comme acceptable pour le jeu.
        """

        difficulty_list = [1, 2]
        filtered = []
        for item in country_data:
            if item["difficulty"] in difficulty_list:
                filtered.append(item)

        return filtered

    def get_name(self, iso):
        """
        Retourne le nom du pays correspondant à un code ISO.

        Paramètres
        ----------
        iso : str
            Code ISO du pays recherché.

        Retour
        ------
        str ou None
            Le nom du pays si trouvé, sinon None.
        """
        data = self.load_country_data()
        for item in data:
            if item["code"] == iso:
                return item["name"]
        return None

    @staticmethod
    def get_flag(iso):
        return str(BASEPATH / "flags" / f"{iso}.png")

    def get_capital(self, iso):
        """
        Retourne le chemin vers l'image du drapeau correspondant au code ISO.

        Paramètres
        ----------
        iso : str
            Code ISO du pays.

        Retour
        ------
        str
            Chemin absolu vers l'image PNG du drapeau.
        """
        data = self.load_country_data()
        for item in data:
            if item["code"] == iso:
                return item["capital"]
        return None

    # Fonctions de jeu :

    def check_answer(
        self, type_quizz, iso, answer, param_all=None
    ):  # dispatcher de mode de jeu
        """
        Vérifie la réponse de l'utilisateur selon le type de quiz.

        Paramètres
        ----------
        type_quizz : str
            Type de quiz ('capitale', 'drapeau', 'tout').
        iso : str
            Code ISO du pays concerné.
        answer : str
            Réponse fournie par l'utilisateur.
        param_all : str, optionnel
            Paramètre interne utilisé pour le mode mixte ('capital' ou 'flag').

        Retour
        ------
        bool
            True si la réponse est correcte, False sinon.
        """

        if type_quizz.lower() == "capitale":
            return self.check_capital(iso, answer)
        elif type_quizz.lower() == "drapeau":
            return self.check_flag(iso, answer)
        elif type_quizz.lower() == "tout":
            if self.param_all == "capital":
                return self.check_capital(iso, answer)
            elif self.param_all == "flag":
                return self.check_flag(iso, answer)

    def check_capital(self, iso, answer):
        """
        Vérifie si la réponse donnée correspond à la capitale du pays.

        Paramètres
        ----------
        iso : str
            Code ISO du pays.
        answer : str
            Réponse de l'utilisateur.

        Retour
        ------
        bool
            True si la réponse est correcte ou tolérée, False sinon.
        """
        country_capital = self.get_capital(iso)
        print(f"bonne reponse : {country_capital.lower()}")
        if self.manage_answer(answer.lower(), country_capital.lower()):
            self.score += 1
            return True
        elif answer.lower() == "debug":
            self.score += 1
            return True
        else:
            self.lives -= 1
            return False

    def check_flag(self, iso, answer):
        """
        Vérifie si la réponse donnée correspond au nom du pays associé au drapeau.

        Paramètres
        ----------
        iso : str
            Code ISO du pays.
        answer : str
            Réponse de l'utilisateur.

        Retour
        ------
        bool
            True si la réponse est correcte ou tolérée, False sinon.
        """
        country_flag = self.get_name(iso)
        print(f"bonne reponse : {country_flag.lower()}")
        if self.manage_answer(answer.lower(), country_flag.lower()):
            self.score += 1
            return True
        elif answer.lower() == "debug":
            self.score += 1
            return True
        else:
            self.lives -= 1
            return False

    def manage_answer(self, answer, data):  # gere la tolerance orthographique
        """
        Compare deux chaînes avec tolérance orthographique.

        Utilise la distance de Levenshtein pour accepter les réponses
        comportant de petites erreurs selon la longueur du mot.

        Paramètres
        ----------
        answer : str
            Réponse de l'utilisateur.
        data : str
            Réponse correcte.

        Retour
        ------
        bool
            True si la réponse est jugée suffisamment proche, False sinon.
        """
        cleaned_answer = self.clean_text(answer)
        cleaned_data = self.clean_text(data)

        nb_error = distance.Levenshtein.distance(cleaned_answer, cleaned_data)

        if len(cleaned_data) < 5:
            if nb_error <= 2:
                return True
            else:
                return (
                    False  # on accepte max 2 erreurs sur les mot de moins de 5 lettres
                )
        else:
            if nb_error <= 3:
                return True
            else:
                return False

    @staticmethod
    def clean_text(text):
        """
        Nettoie une chaîne de texte pour comparaison.

        Supprime les espaces superflus, met en minuscule et retire les accents.

        Paramètres
        ----------
        text : str
            Texte à nettoyer.

        Retour
        ------
        str
            Texte normalisé.
        """
        text = text.strip().lower()  # retrait des espaces et mise en minuscule
        text = " ".join(
            c
            for c in unicodedata.normalize(
                "NFD", text
            )  # nfd (Normalization Form Canonical Decomposition) permet d'indiquer qu'on veut separer les accents de la lettre
            if unicodedata.category(c)
            != "Mn"  # Mn (Mark, Nonspacing) permet d'indiquer qu'on ne veut pas garder les accents
        )
        return text

    def do_reset(self):
        """
        Réinitialise les variables de session du moteur.

        Remet le score à zéro et restaure le nombre de vies initial.
        """
        self.score = 0
        self.lives = 3

    @staticmethod
    def get_filtered_countries(continent, all_data):
        """
        Filtre les pays selon le continent sélectionné.

        Paramètres
        ----------
        continent : str
            Nom du continent ou 'Monde' pour ne rien filtrer.
        all_data : list[dict]
            Liste complète des pays.

        Retour
        ------
        list[dict]
            Liste filtrée des pays.
        """
        if continent == "Monde":
            return all_data
        return [c for c in all_data if c["continents"] == continent]

    @staticmethod
    def save_score(pseudo, score, goalscore, continent, mode, type_quizz):
        """
        Enregistre un score dans le fichier leaderboard.csv.

        Paramètres
        ----------
        pseudo : str
            Nom du joueur.
        score : int
            Score obtenu.
        goalscore : int
            Score maximal possible.
        continent : str
            Continent sélectionné.
        mode : str
            Mode de jeu ('norm' ou 'mar').
        type_quizz : str
            Type de quiz ('Capitale', 'Drapeau', 'Tout').

        Effets
        ------
        Ajoute une ligne au fichier CSV, crée le fichier si nécessaire.
        """

        path = BASEPATH / "leaderboard.csv"

        file_exists = path.exists()  # on check si le fichier existe pour definir plus tard si il faut ajouter les noms de colonnes

        with open(
            path, "a", encoding="utf-8", newline=""
        ) as f:  # a pour append, w supprimerai les anciens scores
            writer = csv.writer(f, delimiter=",")

            if not file_exists:
                writer.writerow(
                    ["pseudo", "score", "goalscore", "continent", "mode", "type_quizz"]
                )

            writer.writerow([pseudo, score, goalscore, continent, mode, type_quizz])

    @staticmethod
    def get_filtered_scores(continent=None, mode=None, type_quizz=None):
        """
        Récupère et filtre les scores enregistrés selon plusieurs critères.

        Paramètres
        ----------
        continent : str, optionnel
        mode : str, optionnel
        type_quizz : str, optionnel

        Retour
        ------
        list[dict]
            Liste triée des meilleurs scores correspondant aux filtres.
        """
        path = BASEPATH / "leaderboard.csv"
        if not path.exists():
            return []

        all_scores = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                cond_cont = continent is None or row["continent"] == continent
                cond_mode = mode is None or row["mode"] == mode
                cond_type = type_quizz is None or row["type_quizz"] == type_quizz

                if cond_cont and cond_mode and cond_type:
                    # On convertit les scores en int pour le tri
                    row["score"] = int(row["score"])
                    row["goalscore"] = int(row["goalscore"])
                    # On calcule le % de réussite pour un tri plus juste si les totaux diffèrent
                    row["percent"] = (row["score"] / row["goalscore"]) * 100
                    all_scores.append(row)

        # TRI : Par pourcentage de réussite, puis par score brut
        all_scores.sort(key=lambda x: (x["percent"], x["score"]), reverse=True)

        return all_scores[:10]

    def create_game_data(self):
        """
        Génère et prépare la liste des pays pour une partie.

        Filtre selon le continent, mélange les données et limite la taille
        selon le mode de jeu.

        Retour
        ------
        tuple
            (liste des pays sélectionnés, taille totale avant filtrage)
        """
        all_data = self.load_country_data()
        data_quizz = self.get_filtered_countries(self.app.continent, all_data)
        self.data_size = len(data_quizz)
        print(f"taille {self.data_size}")
        random.shuffle(data_quizz)

        # limiter la liste pour le mode par défaut
        if self.app.mode == "norm":
            if GOALSCORE > len(data_quizz):
                data_quizz = data_quizz[
                    : len(data_quizz)
                ]  # gestion du cas ou la liste serait plus petite que le goalscore
            else:
                print(data_quizz[:GOALSCORE])
                data_quizz = data_quizz[:GOALSCORE]

        return data_quizz, self.data_size

    def is_endgame(self):
        """
        Détermine si la partie est terminée selon le mode de jeu.

        Retour
        ------
        bool
            True si la partie doit s'arrêter, False sinon.
        """
        print(f" data size : {self.data_size}")
        if self.app.mode == "mar":
            # if len(self.app.question_ui.data_quizz) == 0:
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
        return None
