from pathlib import Path
from kivy.app import App

from PIL import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

import engine

"""
THEME
"""
BACKGROUND_COLOR = "azure3"
MENU_FONT = ('Arial',16, 'bold')
BUTTON_FONT = ('Arial', 12)


""""""
"""
CONSTANTES
"""
BASEPATH = Path(__name__).parent #permet l'utilisation sur tous les systemes
""""""

class Appli(App):
    title = "GéoQuizz"
    icon = 'images/applogo.ico'
    def build(self):
        layout = BoxLayout(orientation='vertical')

        sm = ScreenManager()
        sm.add_widget(afficher_menu())



def afficher_menu(self):
    ...



def afficher_quizz(self):
    ...



def quizz_capitale(self):
    ...

def quizz_flag(self):
    ...

def afficher_game_over(self):
    ...

def afficher_leaderboard(self):
    ...

def main():
    ...

if __name__ == "__main__":
    Appli().run()