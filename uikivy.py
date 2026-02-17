from pathlib import Path
from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.uix import boxlayout
from kivy.uix.image import Image

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout

import engine
from main import Appli

"""
THEME
"""
BACKGROUND_COLOR = "azure3"
MENU_FONT = ('Arial',16, 'bold')
BUTTON_FONT = ('Arial', 12)

# Couleurs du thème (rgba)
NOIR = (0, 0, 0, 1)
BLANC = (1, 1, 1, 1)
ROUGE = (1, 0, 0, 1)
GRIS = (0.2, 0.2, 0.2, 1)
TEAL = (0, 0.5, 0.5, 1)

def label_theme(text, **kwargs):
    return Label(text=text, color=BLANC, size_hint_y=None, height=60,font_size=30, **kwargs)

""""""
"""
CONSTANTES
"""
BASEPATH = Path(__name__).parent #permet l'utilisation sur tous les systemes
""""""


class AfficherMenu(Screen):
    def __init__(self, **kwargs):
        super(AfficherMenu, self).__init__(**kwargs)

        layout = StackLayout(orientation='tb-lr')# tblr => top-bottom, left-right
        self.logo = Image(
            source="images/applogo.png",
            size_hint_y=None,
        )

        with self.logo.canvas.before:  # before pour passer avant (donc en dessous)
            Color(1, 1, 1, 1)  # Blanc
            self.cercle_fond = Ellipse(size=self.logo.size, pos=self.logo.pos)

        self.logo.bind(pos=self.draw_circle, size=self.draw_circle)

        layout.add_widget(self.logo)


        layout.add_widget(
            Button(
                text="Play",
                color=BLANC,
                size_hint_y=None,
                height=60,
                padding=50,
                on_press=self.go_submenu_mode,
            )
        )


        layout.add_widget(
            Button(
                text="Quitter",
                color=BLANC,
                background_color=ROUGE,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )


        self.add_widget(layout)

    def go_submenu_mode(self,instance):         #instance indiqué comme inutilisé mais qd meme necessaire
        self.manager.get_screen('smenu_mode').logo = self.logo
        self.manager.current = 'smenu_mode'



    def draw_circle(self, instance, value):
        diametre = min(instance.size)

        #centrer le cercle
        self.cercle_fond.size = (diametre, diametre)
        self.cercle_fond.pos = (
            instance.center_x - diametre / 2,
            instance.center_y - diametre / 2
        )



class SubmenuMode(Screen):
    def __init__(self, **kwargs):
        super(SubmenuMode, self).__init__(**kwargs)
        self.logo = None
        self.mode = None

        layout = StackLayout(orientation='tb-lr')  # tblr => top-bottom, left-right

        #layout.add_widget(self.logo)

        layout.add_widget(
            Button(
                text="Marathon",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=self.go_submenu_cont_by_mar
            )
        )

        layout.add_widget(
            Button(
                text="Normal",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=self.go_submenu_cont_by_norm
            )
        )

        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press=self.go_back
            )
        )

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = self.manager.previous()

    def go_submenu_cont_by_mar(self,instance):
        self.manager.current = 'smenu_cont'

    def go_submenu_cont_by_norm(self,instance):
        self.manager.current = 'smenu_cont'




class SubmenuCont(Screen):
    def __init__(self, **kwargs):
        super(SubmenuCont, self).__init__(**kwargs)

        layout = StackLayout(orientation='tb-lr')  # tblr => top-bottom, left-right

        #layout.add_widget(self.logo)

        layout.add_widget(
            Button(
                text="Monde",
                color=BLANC,
                size_hint_y=None,
                height=60,
            )
        )

        layout.add_widget(
            Button(
                text="Afrique",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )

        layout.add_widget(
            Button(
                text="Amériques",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )

        layout.add_widget(
            Button(
                text="Asie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )

        layout.add_widget(
            Button(
                text="Europe",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )

        layout.add_widget(
            Button(
                text="Océanie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop
            )
        )

        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press=self.go_back
            )
        )

        self.add_widget(layout)



    def go_back(self, instance):
        self.manager.current = self.manager.previous()


    def draw_circle(self, instance, value):
        diametre = min(instance.size)

        # centrer le cercle
        self.cercle_fond.size = (diametre, diametre)
        self.cercle_fond.pos = (
            instance.center_x - diametre / 2,
            instance.center_y - diametre / 2
        )






def afficher_quizz(self):
    def __init__(self, **kwargs):
        super(AfficherMenu, self).__init__(**kwargs)

        #va appeler les bonnes fonctions de jeux en fonction de mode et continent



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

