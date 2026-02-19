from pathlib import Path
from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.properties import StringProperty
from kivy.uix import boxlayout
from kivy.uix.image import Image

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.slider import Slider
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

import engine
from main import Appli

"""
THEME
"""


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

class BaseScreen(Screen): #semble être la méthode la plus appropriée pour gerer le passage de variable. De plus la génération auto a directmeent compris
    @property
    def app(self):
        return App.get_running_app()


class DrawLogo(RelativeLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 100)
        super(DrawLogo, self).__init__(**kwargs)

        with self.canvas.before:
            Color(BLANC)  # Blanc
            self.cercle_fond = Ellipse()

        # 2. L'image du logo
        self.image = Image(source="images/applogo.png")
        self.add_widget(self.image)

        # 3. On lie le redimensionnement
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, instance, value):
        diametre = min(self.size)
        self.cercle_fond.size = (diametre, diametre)
        # On centre dans le RelativeLayout
        self.cercle_fond.pos = (
            (self.width - diametre) / 2,
            (self.height - diametre) / 2
        )



class AfficherMenu(BaseScreen):
    def __init__(self, **kwargs):
        super(AfficherMenu, self).__init__(**kwargs)

        layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)# tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

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
        #self.app.root.transition = SlideTransition(direction="left")
        #self.manager.current = 'smenu_mode'
        self.app.root.current = 'smenu_mode' #self.app.root est le scrren manager



class SubmenuMode(BaseScreen):
    def __init__(self, **kwargs):
        super(SubmenuMode, self).__init__(**kwargs)
        self.logo = None
        self.mode = None

        layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)  # tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

        layout_pseudo = BoxLayout(orientation='horizontal', padding = 20, spacing = 20, height = 50, size_hint_y = None)
        self.pseudo_label = Label(text="Pseudo : ", size_hint_y=None, height=30)
        self.input_pseudo = TextInput(text=self.app.pseudo, multiline=False, size_hint_y=None, height = 30)
        layout_pseudo.add_widget(self.pseudo_label)
        layout_pseudo.add_widget(self.input_pseudo)
        layout.add_widget(layout_pseudo)#textinput

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

    def on_pre_enter(self, *args):
        ...

    def go_back(self, instance):
        self.app.root.current = self.manager.previous()

    def go_submenu_cont_by_mar(self,instance):
        self.app.mode = 'mar'
        self.app.pseudo = self.input_pseudo.text
        self.app.root.current = 'smenu_cont'

    def go_submenu_cont_by_norm(self,instance):
        self.app.mode = 'norm'
        self.app.pseudo = self.input_pseudo.text
        self.app.root.current = 'smenu_cont'

    def update_pseudo(self, instance, value):
        self.app.pseudo = self.input_pseudo.text




class SubmenuCont(BaseScreen):
    def __init__(self, **kwargs):
        super(SubmenuCont, self).__init__(**kwargs)

        layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)  # tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

        self.label_mode = Label(text="",size_hint_y=None, height=40)

        self.label_pseudo = Label(text="", size_hint_y=None, height=30)

        layout.add_widget(self.label_pseudo)

        layout.add_widget(self.label_mode)


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

    def on_pre_enter(self):
        print(self.app.mode)
        if self.app.mode == 'mar':
            self.label_mode.text = 'Mode Marathon'
        elif self.app.mode == 'norm':
            self.label_mode.text = 'Mode Normal'

        self.label_pseudo.text = f"Pseudo : {self.app.pseudo}"





    def on_press(self):
        #self.label_mode = self.app.mode
        ...

    def go_back(self, instance):
        self.app.root.current = self.manager.previous()


    # def draw_circle(self, instance, value):
    #     diametre = min(instance.size)
    #
    #     # centrer le cercle
    #     self.cercle_fond.size = (diametre, diametre)
    #     self.cercle_fond.pos = (
    #         instance.center_x - diametre / 2,
    #         instance.center_y - diametre / 2
    #     )






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

