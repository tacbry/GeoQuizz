from pathlib import Path
from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import StringProperty
from kivy.uix import boxlayout
from kivy.uix.anchorlayout import AnchorLayout
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

        self.image = Image(source="images/applogo.png")
        self.add_widget(self.image)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, instance, value):
        diametre = min(self.size)
        self.cercle_fond.size = (diametre, diametre)
        # On centre dans le RelativeLayout
        self.cercle_fond.pos = (
            (self.width - diametre) / 2,
            (self.height - diametre) / 2
        )


class WhiteLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", NOIR)
        super(WhiteLabel, self).__init__(**kwargs)

        with self.canvas.before:
            self.background_color = BLANC
            self.rect = Rectangle()

        self.bind(pos=self.update_graphics, size=self.update_graphics)


    def update_graphics(self, instance, value):
        self.rect.pos = (self.x + 1, self.y + 1)
        self.rect.size = (self.width - 2 , self.height - 2)

class DrawBoard(BoxLayout): #centralise l'affichage des choxi
    def __init__(self, **kwargs ):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 75)
        kwargs.setdefault("padding", 40)
        kwargs.setdefault("orientation",'horizontal')

        super(DrawBoard, self).__init__(**kwargs)

        #label pseudo
        self.label_pseudo = WhiteLabel(text="", size_hint_y=None, size_hint_x= 1, height=40)
        self.add_widget(self.label_pseudo)

        # label mode
        self.label_mode = WhiteLabel(text="",size_hint_y=None, size_hint_x= 1, height=40)
        self.add_widget(self.label_mode)


        #label continent
        self.label_continent = WhiteLabel(text="", size_hint_y=None, size_hint_x= 1, height=40)
        self.add_widget(self.label_continent)


        #label type quiz
        self.label_quiz_type = WhiteLabel(text="", size_hint_y=None, size_hint_x= 1, height=40)
        self.add_widget(self.label_quiz_type)


    def update_labels(self, show_pseudo = False,show_mode = False, show_continent = False, show_type = False, **kwargs):
        if show_mode:
            if App.get_running_app().mode == 'mar':
                self.label_mode.text = 'Mode Marathon'
            elif App.get_running_app().mode == 'norm':
                self.label_mode.text = 'Mode Normal'

        if show_pseudo:
            self.label_pseudo.text = f"Pseudo : {App.get_running_app().pseudo}"

        if show_continent:
            self.label_continent.text = App.get_running_app().continent

        if show_type:
            self.label_quiz_type.text = App.get_running_app().type_quizz #c

    def update_rect (self, instance,value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class AfficherMenu(BaseScreen):
    def __init__(self, **kwargs):
        super(AfficherMenu, self).__init__(**kwargs)

        layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)# tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

        layout.add_widget(
            Button(
                text="Jouer",
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

        self.board = DrawBoard()
        layout.add_widget(self.board)


        layout.add_widget(
            Button(
                text="Monde",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x : self.go_next(self, continent= 'Monde')
            )
        )

        layout.add_widget(
            Button(
                text="Afrique",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x : self.go_next(self, continent= 'Afrique')
            )
        )

        layout.add_widget(
            Button(
                text="Amériques",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x : self.go_next(self, continent= 'Amériques')
            )
        )

        layout.add_widget(
            Button(
                text="Asie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x : self.go_next(self, continent= 'Asie')
            )
        )

        layout.add_widget(
            Button(
                text="Europe",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x : self.go_next(self, continent= 'Europe')
            )
        )


        layout.add_widget(
            Button(
                text="Océanie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press= lambda x : self.go_next(self, continent= 'Océanie')
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
        self.board.update_labels(show_pseudo=True, show_mode = True)



    def go_next(self, instance , continent):
        self.app.continent = continent
        self.app.root.current = 'smenu_quizz-type'



    def go_back(self, instance):
        self.app.root.current = self.manager.previous()

class SubmenuQuizzType(BaseScreen):
    def __init__(self, **kwargs):
        super(SubmenuQuizzType, self).__init__(**kwargs)
        layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)

        layout.add_widget(DrawLogo())

        self.board = DrawBoard()
        layout.add_widget(self.board)

        layout.add_widget(
            Button(
                text="Capitale",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press= lambda x :self.go_next(self, type_quizz= 'Capitale')
            )
        )

        layout.add_widget(
            Button(
                text="Drapeau",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press= lambda x :self.go_next(self, type_quizz= 'Drapeau')
            )
        )

        layout.add_widget(
            Button(
                text="Tout",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press= lambda x :self.go_next(self, type_quizz= 'Tout')
            )
        )


        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press= self.go_back
            )
        )




        self.add_widget(layout)



    def on_pre_enter(self):
        self.board.update_labels(show_pseudo=True, show_mode = True, show_continent = True)



    def go_next(self, instance , type_quizz):
        self.app.type_quizz = type_quizz
        self.app.root.current = 'show-quizz'


    def go_back(self, instance):
        self.app.root.current = self.manager.previous()

class ShowQuizz(BaseScreen):
    def __init__(self, **kwargs):
        super(ShowQuizz, self).__init__(**kwargs)

        #layout de base
        #self.flag = None
        self.answer = None
        self.input_answer = None
        self.flag = None
        self.country_name_label = None
        self.type_quizz = None

        self.layout = StackLayout(orientation='tb-lr', padding = 20, spacing = 20)
        #self.layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=(1,None), height=250)

        self.layout.add_widget(Button(
            text="Home",
            color=BLANC,
            background_color=TEAL,
            size_hint_y=None,
            height=60,
            on_press=self.go_home
        ))

        self.layout.add_widget(DrawLogo())

        self.board = DrawBoard()
        self.layout.add_widget(self.board)

        self.create_quizz_capitale()
        print(self.type_quizz)
        if self.type_quizz == 'Capitale':
            self.create_quizz_capitale()

        elif self.type_quizz == 'Drapeau':
            self.create_quizz_drapeau()

        elif self.type_quizz == 'Tout':
            ...





        self.add_widget(self.layout)


        #pop up pour confirmer, quitter la fenetre declenche le jeu


    def on_pre_enter(self):
        self.board.update_labels(show_pseudo=True, show_mode = True, show_continent = True, show_type = True)
        self.type_quizz = self.app.type_quizz

    def go_home(self, instance):
        self.app.root.current = 'menu'



    def create_quizz_capitale(self):
        layout = BoxLayout(orientation='vertical', size_hint=(1,None), height=400)

        self.country_name_label = Label(text=engine.get_name('AD'), size_hint_y=None, height=50)
        layout.add_widget(self.country_name_label)
        self.flag = Image(source=engine.get_flag('AD'),
                          size_hint=(None, None),
                          size=(200, 150), pos_hint={'center_x': .5})
        layout.add_widget(self.flag)

        answer_layout = BoxLayout(orientation='horizontal', size_hint=(1,None), height=200)

        self.input_answer = TextInput(text="", multiline=False, size_hint_y=None, height=30, on_text_validate=self.validate)


        answer_layout.add_widget(self.input_answer)




        answer_layout.add_widget(Button(
            text="Valider",
            color=BLANC,
            background_color=TEAL,
            size_hint_y=None,
            height=60,
            on_press=self.validate)
        )

        layout.add_widget(answer_layout)



        # layout.add_widget(Button(
        #     text="Retour",
        #     color=BLANC,
        #     background_color=TEAL,
        #     size_hint_y=None,
        #     height=60,
        #     on_press=self.validate())
        # )

        self.layout.add_widget(layout)

    def validate(self, instance):
        self.answer = str(self.input_answer.text)
        engine.play_capitals('AD')
        print(self.answer)







    def quizz_flag(self):
        ...

def afficher_game_over(self):
    ...

def afficher_leaderboard(self):
    ...

def main():
    ...

