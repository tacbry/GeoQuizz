from pathlib import Path
import random
from kivy.clock import Clock

from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

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
    return Label(
        text=text, color=BLANC, size_hint_y=None, height=60, font_size=30, **kwargs
    )


""""""
"""
CONSTANTES
"""
BASEPATH = Path(__name__).parent  # permet l'utilisation sur tous les systemes
GOALSCORE = 15
""""""


class BaseScreen(
    Screen
):  # semble être la méthode la plus appropriée pour gerer le passage de variable. De plus la génération auto a directmeent compris
    """Base class for all application screens.

    Fournit un accès simplifié à l'application via la propriété `app`,
    permettant aux écrans d'accéder aux variables globales (pseudo, mode,
    continent, moteur de jeu, etc.).
    """

    @property
    def app(self):
        """
        Retourne l'event de l'application Kivy en cours.

        Permet d'accéder facilement aux variables globales de l'application
        (pseudo, mode, continent, moteur de jeu, etc.) depuis n'importe quel écran.
        """
        return App.get_running_app()


class DrawLogo(RelativeLayout):
    """Widget affichant le logo circulaire de l'application.

    Dessine un cercle blanc en arrière-plan et centre automatiquement
    l'image du logo à l'intérieur, en s'adaptant aux changements de taille.
    """

    def __init__(self, **kwargs):
        """
        Initialise le widget du logo circulaire.

        Crée un cercle blanc en arrière-plan et place l'image du logo au centre.
        Le cercle s'adapte automatiquement à la taille du widget.
        """
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 100)
        super(DrawLogo, self).__init__(**kwargs)

        with self.canvas.before:
            Color(BLANC)  # Blanc
            self.cercle_fond = Ellipse()

        self.image = Image(source="images/applogo.png")
        self.add_widget(self.image)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, event, value):
        """
        Met à jour la taille et la position du cercle de fond.

        Appelé automatiquement lorsque le widget change de taille ou de position.
        Le cercle reste toujours centré et parfaitement circulaire.

            Args:
        event: Widget déclencheur.
        value: Nouvelle valeur de taille ou position.
        """
        diametre = min(self.size)
        self.cercle_fond.size = (diametre, diametre)
        # On centre dans le RelativeLayout
        self.cercle_fond.pos = (
            (self.width - diametre) / 2,
            (self.height - diametre) / 2,
        )


class WhiteLabel(Label):
    """Label personnalisé avec un fond blanc.

    Ajoute un rectangle blanc derrière le texte pour créer un effet visuel
    de mise en avant, utile pour les tableaux d'informations.
    """

    def __init__(self, **kwargs):
        """
        Initialise un label avec un fond blanc.

        Ajoute un rectangle en arrière-plan pour créer un effet de bouton ou de zone
        mise en avant dans l'interface.
        """
        kwargs.setdefault("color", NOIR)
        super(WhiteLabel, self).__init__(**kwargs)

        with self.canvas.before:
            self.background_color = BLANC
            self.rect = Rectangle()

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, event, value):
        """
        Met à jour la taille et la position du rectangle de fond.

        Garantit que le fond blanc suit toujours les dimensions du label.

            Args:
        instance: Widget déclencheur.
        value: Nouvelle valeur de taille ou position.

        """
        self.rect.pos = (self.x + 1, self.y + 1)
        self.rect.size = (self.width - 2, self.height - 2)


class DrawBoard(BoxLayout):  # centralise l'affichage des choxi
    """Tableau d'informations affichant les paramètres de la partie.

    Contient quatre labels : pseudo, mode de jeu, continent et type de quiz.
    Les valeurs sont mises à jour dynamiquement selon l'écran affiché.
    """

    def __init__(self, **kwargs):
        """
        Initialise le tableau d'informations affichant pseudo, mode, continent et type de quiz.

        Crée quatre labels alignés horizontalement, chacun pouvant être mis à jour
        selon les besoins de l'écran courant.
        """
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", 75)
        kwargs.setdefault("padding", 40)
        kwargs.setdefault("orientation", "horizontal")

        super(DrawBoard, self).__init__(**kwargs)

        # label pseudo
        self.label_pseudo = WhiteLabel(
            text="", size_hint_y=None, size_hint_x=1, height=40
        )
        self.add_widget(self.label_pseudo)

        # label mode
        self.label_mode = WhiteLabel(
            text="", size_hint_y=None, size_hint_x=1, height=40
        )
        self.add_widget(self.label_mode)

        # label continent
        self.label_continent = WhiteLabel(
            text="", size_hint_y=None, size_hint_x=1, height=40
        )
        self.add_widget(self.label_continent)

        # label type quiz
        self.label_quiz_type = WhiteLabel(
            text="", size_hint_y=None, size_hint_x=1, height=40
        )
        self.add_widget(self.label_quiz_type)

    def update_labels(
        self,
        show_pseudo=False,
        show_mode=False,
        show_continent=False,
        show_type=False,
        **kwargs,
    ):
        """
        Met à jour dynamiquement les labels du tableau d'informations.

        Paramètres
        ----------
        show_pseudo : bool
            Affiche ou non le pseudo du joueur.
        show_mode : bool
            Affiche ou non le mode de jeu.
        show_continent : bool
            Affiche ou non le continent sélectionné.
        show_type : bool
            Affiche ou non le type de quiz choisi.
        """

        if show_mode:
            if App.get_running_app().mode == "mar":
                self.label_mode.text = "Mode Marathon"
            elif App.get_running_app().mode == "norm":
                self.label_mode.text = "Mode par défaut"

        if show_pseudo:
            self.label_pseudo.text = f"Pseudo : {App.get_running_app().pseudo}"

        if show_continent:
            self.label_continent.text = App.get_running_app().continent

        if show_type:
            self.label_quiz_type.text = App.get_running_app().type_quizz

    def update_rect(self):
        """
        Met à jour la taille et la position du rectangle de fond.

        Utilisé si un fond graphique est ajouté derrière le tableau.
        """

        self.rect.pos = self.pos
        self.rect.size = self.size


class AfficherMenu(BaseScreen):
    """Écran principal du menu de l'application.

    Affiche le logo, les boutons Jouer, Hall of Fame et Quitter.
    Sert de point d'entrée pour la navigation dans l'application.
    """

    def __init__(self, **kwargs):
        """
        Initialise l'écran du menu principal.

        Affiche le logo, les boutons Jouer, Hall of Fame et Quitter.
        """
        super(AfficherMenu, self).__init__(**kwargs)

        layout = StackLayout(
            orientation="tb-lr", padding=20, spacing=20
        )  # tblr => top-bottom, left-right

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
                text="Hall of fame",
                color=BLANC,
                size_hint_y=None,
                height=60,
                padding=50,
                on_press=self.go_leaderboard,
            )
        )

        layout.add_widget(
            Button(
                text="Quitter",
                color=BLANC,
                background_color=ROUGE,
                size_hint_y=None,
                height=60,
                on_press=App.get_running_app().stop,
            )
        )

        self.add_widget(layout)

    def go_submenu_mode(
        self, event
    ):  # event indiqué comme inutilisé mais qd meme necessaire
        """
        Navigue vers le sous-menu de sélection du mode de jeu.
        """
        # self.app.root.transition = SlideTransition(direction="left")
        self.app.root.current = "smenu_mode"  # self.app.root est le scrren manager

    def go_leaderboard(self, event):
        """
        Ouvre l'écran d'affichage du classement.
        """
        self.app.root.current = "show-lb"


class SubmenuMode(BaseScreen):
    """Écran de sélection du mode de jeu.

    Permet au joueur de saisir son pseudo et de choisir entre le mode
    normal et le mode marathon avant de poursuivre vers la sélection
    du continent.
    """

    def __init__(self, **kwargs):
        """
        Initialise l'écran de sélection du mode de jeu.

        Permet au joueur de saisir son pseudo et de choisir entre
        le mode par défaut et le mode marathon.
        """
        super(SubmenuMode, self).__init__(**kwargs)
        self.logo = None
        self.mode = None

        layout = StackLayout(
            orientation="tb-lr", padding=20, spacing=20
        )  # tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

        layout_pseudo = BoxLayout(
            orientation="horizontal",
            padding=20,
            spacing=20,
            height=50,
            size_hint_y=None,
        )
        self.pseudo_label = Label(text="Pseudo : ", size_hint_y=None, height=30)
        self.input_pseudo = TextInput(
            text=self.app.pseudo, multiline=False, size_hint_y=None, height=40
        )
        layout_pseudo.add_widget(self.pseudo_label)
        layout_pseudo.add_widget(self.input_pseudo)
        layout.add_widget(layout_pseudo)  # textinput

        layout.add_widget(
            Button(
                text="Par défaut",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=self.go_submenu_cont_by_norm,
            )
        )

        layout.add_widget(
            Button(
                text="Marathon",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=self.go_submenu_cont_by_mar,
            )
        )

        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press=self.go_back,
            )
        )

        self.add_widget(layout)

    def go_back(self, event):
        """
        Retourne à l'écran précédent dans le ScreenManager.
        """
        self.app.root.current = self.manager.previous()

    def go_submenu_cont_by_mar(self, event):
        """
        Active le mode Marathon et navigue vers la sélection du continent.
        """
        self.app.mode = "mar"
        self.app.pseudo = self.input_pseudo.text
        self.app.root.current = "smenu_cont"

    def go_submenu_cont_by_norm(self, event):
        """
        Active le mode par défaut et navigue vers la sélection du continent.
        """
        self.app.mode = "norm"
        self.app.pseudo = self.input_pseudo.text
        self.app.root.current = "smenu_cont"

    def update_pseudo(self, event, value):
        """
        Met à jour le pseudo du joueur dans l'application.

        Appelé lorsque le champ de texte est modifié.
        """
        self.app.pseudo = self.input_pseudo.text


class SubmenuCont(BaseScreen):
    """Écran de sélection du continent.

    Propose les différents continents disponibles pour filtrer les pays
    du quiz. Affiche également un tableau récapitulatif des paramètres
    déjà choisis.
    """

    def __init__(self, **kwargs):
        """
        Initialise l'écran de sélection du continent.

        Affiche les boutons pour chaque continent ainsi que le tableau d'informations.
        """
        super(SubmenuCont, self).__init__(**kwargs)

        layout = StackLayout(
            orientation="tb-lr", padding=20, spacing=20
        )  # tblr => top-bottom, left-right

        layout.add_widget(DrawLogo())

        self.board = DrawBoard()
        layout.add_widget(self.board)

        layout.add_widget(
            Button(
                text="Monde",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="Monde"),
            )
        )

        layout.add_widget(
            Button(
                text="Afrique",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="Africa"),
            )
        )

        layout.add_widget(
            Button(
                text="Amériques",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="America"),
            )
        )

        layout.add_widget(
            Button(
                text="Asie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="Asia"),
            )
        )

        layout.add_widget(
            Button(
                text="Europe",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="Europe"),
            )
        )

        layout.add_widget(
            Button(
                text="Océanie",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, continent="Oceania"),
            )
        )

        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press=self.go_back,
            )
        )

        self.add_widget(layout)

    def on_pre_enter(self):
        """
        Met à jour les informations affichées avant l'entrée sur l'écran.

        Affiche le pseudo et le mode sélectionné.
        """

        self.board.update_labels(show_pseudo=True, show_mode=True)

    def go_next(self, event, continent):
        """
        Enregistre le continent choisi et navigue vers la sélection du type de quiz.

            Args:
        instance: Bouton déclencheur.
        continent (str): Continent choisi.

        """
        self.app.continent = continent
        self.app.root.current = "smenu_quizz-type"

    def go_back(self, event):
        """
        Retourne à l'écran précédent.
        """
        self.app.root.current = self.manager.previous()


class SubmenuQuizzType(BaseScreen):
    """Écran de sélection du type de quiz.

    Permet de choisir entre un quiz sur les capitales, les drapeaux
    ou un mode mixte combinant les deux.
    """

    def __init__(self, **kwargs):
        """
        Initialise l'écran de sélection du type de quiz.

        Permet de choisir entre Capitale, Drapeau ou Tout.
        """
        super(SubmenuQuizzType, self).__init__(**kwargs)
        layout = StackLayout(orientation="tb-lr", padding=20, spacing=20)

        layout.add_widget(DrawLogo())

        self.board = DrawBoard()
        layout.add_widget(self.board)

        layout.add_widget(
            Button(
                text="Capitale",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, type_quizz="Capitale"),
            )
        )

        layout.add_widget(
            Button(
                text="Drapeau",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, type_quizz="Drapeau"),
            )
        )

        layout.add_widget(
            Button(
                text="Tout",
                color=BLANC,
                size_hint_y=None,
                height=60,
                on_press=lambda x: self.go_next(self, type_quizz="Tout"),
            )
        )

        layout.add_widget(
            Button(
                text="Retour",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=60,
                on_press=self.go_back,
            )
        )
        self.add_widget(layout)

    def on_pre_enter(self):
        """
        Met à jour les informations affichées avant l'entrée sur l'écran.

        Affiche pseudo, mode et continent.
        """
        self.board.update_labels(show_pseudo=True, show_mode=True, show_continent=True)

    def go_next(self, event, type_quizz):
        """
        Enregistre le type de quiz choisi et lance l'écran du quiz.
            Args:
        instance: Bouton déclencheur.
        type_quizz (str): Type de quiz choisi.
        """
        self.app.type_quizz = type_quizz
        self.app.root.current = "show-quizz"

    def go_back(self, event):
        """
        Retourne à l'écran précédent.
        """
        self.app.root.current = self.manager.previous()


class ShowQuizz(BaseScreen):
    """Écran principal du quiz.

    Gère l'affichage des questions, la saisie des réponses, la progression
    du joueur, le score, les vies restantes et la logique de fin de partie.
    """

    def __init__(self, **kwargs):
        """
        Initialise l'écran du quiz.

        Prépare la zone d'affichage des questions et les variables nécessaires
        au déroulement de la partie.
        """

        super(ShowQuizz, self).__init__(**kwargs)

        self.input_answer = None
        self.lives_label = None
        self.data_size = None
        self.flag = None
        self.score_label = None
        self.type_quizz = None
        self.goal_score = None
        self.answer = None
        self.country_name_label = None
        self.current_country = None
        self.data_quizz = []

        # creation du layout de base
        self.question_layout = StackLayout(orientation="tb-lr", padding=20, spacing=20)
        self.add_widget(self.question_layout)

    def on_pre_enter(self):  # prepare les données de jeu
        """
        Prépare les données du quiz avant l'affichage de l'écran.

        Charge la liste des pays filtrés, initialise la progression
        et génère la première question.
        """

        self.data_quizz = self.app.engine.create_game_data()[0]
        self.data_size = self.app.engine.create_game_data()[1]
        print(self.data_quizz)
        print(self.data_size)

        if self.app.mode == "mar":
            self.goal_score = self.data_size
        elif self.app.mode == "norm":
            self.goal_score = GOALSCORE

        self.next_question()

    def on_enter(self, *args):
        """
        Méthode appelée lorsque l'écran devient visible.

        Utilisée pour gérer le focus automatique du champ de réponse.
        """
        Clock.schedule_once(lambda dt: setattr(self.input_answer, "focus", True))
        # permet le focus sur la premiere slide

    def next_question(self):
        """
        Génère la question suivante du quiz.

        Met à jour la progression, sélectionne un nouveau pays et
        construit l'interface de la question correspondante.
        """
        # verifie si fin de partie avant de creer la question
        if self.app.engine.is_endgame():
            print("DEBUG : fin next qu")
            self.game_over()  # pas de do reset avant d'avoir save le score dans le fichier
            return

        self.current_country = self.data_quizz.pop()
        self.question_layout.clear_widgets()

        self.app.engine.data_size = len(self.data_quizz)
        current_mode = self.app.type_quizz.lower()

        # reinitialisation du paramtre a chaque question

        if current_mode == "tout":
            self.app.engine.param_all = random.choice(["capital", "flag"])
        else:
            self.app.engine.param_all = None

        if self.app.mode == "mar":
            self.goal_score = self.data_size
        else:
            self.goal_score = GOALSCORE

        self.create_quizz(self.current_country["code"])

    def go_home(self):
        """
        Retourne à l'écran d'accueil.
        """

        self.app.root.current = "menu"

    def create_quizz(self, iso):
        """
        Construit l'interface d'une question de quiz.

        Affiche le drapeau, le nom du pays ou la question selon le mode,
        ainsi qu'un champ de réponse et un bouton de validation.

            Args:
        iso (str): Code ISO du pays concerné.
        """

        is_capital_mode = (
            self.app.engine.param_all == "capital"
            or self.app.type_quizz.lower() == "capitale"
        )

        layout = BoxLayout(orientation="vertical", size_hint=(1, None), height=500)

        top_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)

        self.pseudo_label = Label(
            text=f"{self.app.pseudo}", size_hint_y=None, height=50
        )
        top_layout.add_widget(self.pseudo_label)

        if self.app.mode == "mar":
            self.score_label = Label(
                text=f"{self.app.engine.score} / {self.goal_score - self.app.engine.data_size - 1} ({self.app.engine.data_size} restants)",
                size_hint_y=None,
                height=50,
            )

        else:
            self.score_label = Label(
                text=f"{self.app.engine.score} / {self.goal_score}",
                size_hint_y=None,
                height=50,
            )

        top_layout.add_widget(self.score_label)

        self.lives_label = Label(
            text=f"Vies restantes : {self.app.engine.lives}",
            size_hint_y=None,
            height=50,
        )
        top_layout.add_widget(self.lives_label)

        layout.add_widget(top_layout)

        if is_capital_mode:
            self.country_name_label = Label(
                text=self.app.engine.get_name(iso), size_hint_y=None, height=50
            )
            layout.add_widget(self.country_name_label)
        else:
            layout.add_widget(
                Label(size_hint_y=None, height=50)
            )  # espace vide pour maitenir les hauteurs cohérentes

        self.flag = Image(
            source=self.app.engine.get_flag(iso),
            size_hint=(None, None),
            size=(200, 150),
            pos_hint={"center_x": 0.5},
        )
        layout.add_widget(self.flag)

        # question

        question_text = "Capitale ?" if is_capital_mode else "Pays ?"
        layout.add_widget(Label(text=question_text, size_hint_y=None, height=50))

        # reponse
        answer_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=200,
            padding=10,
            spacing=10,
        )

        self.input_answer = TextInput(
            text="",
            multiline=False,
            size_hint_y=None,
            height=50,
            on_text_validate=self.validate,
        )
        answer_layout.add_widget(self.input_answer)

        answer_layout.add_widget(
            Button(
                text="Valider",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=50,
                on_press=self.validate,
            )
        )

        layout.add_widget(answer_layout)

        self.question_layout.add_widget(layout)
        Clock.schedule_once(lambda dt: setattr(self.input_answer, "focus", True))

    def validate(self, event):
        """Validate the user's answer and load the next question.

        Args:
            instance: Bouton ou TextInput déclencheur.
        """
        if self.app.engine.check_answer(
            type_quizz=self.app.type_quizz,
            iso=self.current_country["code"],
            answer=self.input_answer.text,
        ):
            print("bonne reponse")
            print(f"{self.app.engine.score} points")
            self.next_question()
        else:
            self.next_question()

    def game_over(self):
        """Display the end-of-game screen with final score and options."""

        # on relie à question layout car c'est celui la qui est créé de base.
        self.question_layout.clear_widgets()

        layout = BoxLayout(orientation="vertical", size_hint=(1, None), height=450)

        layout.add_widget(Label(text=f"fin de partie", size_hint_y=None, height=50))
        layout.add_widget(Label(text=f"Score", size_hint_y=None, height=50))

        score_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=50
        )
        score_layout.add_widget(
            Label(text=f"{self.app.pseudo}", size_hint_y=None, height=50)
        )
        score_layout.add_widget(
            Label(
                text=f"{self.app.engine.score} / {self.goal_score}",
                size_hint_y=None,
                height=50,
            )
        )

        layout.add_widget(score_layout)

        btn_layout = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=450
        )
        btn_layout.add_widget(
            Button(
                text="Acceuil",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=50,
                on_press=lambda kdb: self.end_game("home"),
            )
        )

        btn_layout.add_widget(
            Button(
                text="Hall of Fame",
                color=BLANC,
                background_color=TEAL,
                size_hint_y=None,
                height=50,
                on_press=lambda kdb: self.end_game("lb"),
            )
        )

        layout.add_widget(btn_layout)

        self.question_layout.add_widget(layout)

    def end_game(self, target):
        """Save the final score and navigate to the chosen screen.

        Args:
            target (str): 'home' pour menu, 'lb' pour leaderboard.
        """
        self.app.engine.save_score(
            pseudo=self.app.pseudo,
            # score= self.score_label.text, #voir si je garde ca ou bien si je divise et que je prends self.app.engine.score
            score=self.app.engine.score,
            goalscore=GOALSCORE,
            continent=self.app.continent,
            mode=self.app.mode,
            type_quizz=self.app.type_quizz,
        )

        self.app.engine.do_reset()

        if target == "home":
            self.go_home()
        if target == "lb":
            self.go_leaderboard()

    def go_leaderboard(self):
        """Navigate to the leaderboard screen."""
        self.app.root.current = "show-lb"


class ShowLeaderboard(BaseScreen):
    """Écran d'affichage du classement.

    Permet de filtrer les scores enregistrés selon le continent, le mode
    de jeu et le type de quiz. Affiche les meilleurs résultats sous forme
    de tableau.
    """

    def __init__(self, **kwargs):
        """Initialize the leaderboard screen.

        Crée les filtres (continent, mode, type de quiz) et la table des scores.
        """

        super(ShowLeaderboard, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # barre de filtres
        self.filters_layout = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=10
        )

        # On définit les options (doivent matcher avec les valeurs de ton CSV)
        self.spin_cont = Spinner(
            text="Monde",
            values=("Monde", "Africa", "America", "Asia", "Europe", "Oceania"),
        )
        self.spin_mode = Spinner(text="Par défaut", values=("Par défaut", "Marathon"))
        self.spin_type = Spinner(
            text="Capitale", values=("Capitale", "Drapeau", "Tout")
        )

        # on lie le changement de texte à updateview
        self.spin_cont.bind(text=self.update_view)
        self.spin_mode.bind(text=self.update_view)
        self.spin_type.bind(text=self.update_view)

        self.filters_layout.add_widget(self.spin_cont)
        self.filters_layout.add_widget(self.spin_mode)
        self.filters_layout.add_widget(self.spin_type)

        self.layout.add_widget(self.filters_layout)

        # tableau des scores (en scrollview)
        self.scroll = ScrollView(size_hint=(1, 1))
        self.score_table = GridLayout(cols=4, size_hint_y=None, spacing=5)
        self.score_table.bind(
            minimum_height=self.score_table.setter("height")
        )  # permet d'adapter auto la taille du layout a son contenu
        # self.score_table.bind()

        self.scroll.add_widget(self.score_table)
        self.layout.add_widget(self.scroll)

        self.layout.add_widget(
            Button(text="Retour", size_hint_y=None, height=50, on_press=self.go_back)
        )

        self.add_widget(self.layout)

    def on_pre_enter(self):
        """Load and display scores when entering the screen."""

        # Initialise la vue au chargement de l'écran
        self.update_view()

    def go_back(self, event):
        """Return to the main menu.

        Args:
            instance: Bouton déclencheur.
        """
        self.app.root.current = "menu"

    def update_view(self, *args):
        """Refresh the leaderboard according to selected filters."""
        # on clean les scores à chaque update
        self.score_table.clear_widgets()

        cont = self.spin_cont.text
        # ajustement pour permettre l'affichage des bons noms dans menu deroulant mode
        if self.spin_mode.text == "Marathon":
            mode = "mar"
        elif self.spin_mode.text == "Par défaut":
            mode = "norm"
        quizz = self.spin_type.text

        data = self.app.engine.get_filtered_scores(
            continent=cont, mode=mode, type_quizz=quizz
        )

        # contruction du header
        self.add_header()

        # affichage des scores
        if not data:
            self.score_table.add_widget(
                Label(text="Aucun score", size_hint_y=None, height=40)
            )
            # On ajoute des labels vides pour remplir les 3 colonnes restantes de la ligne
            for _ in range(3):
                self.score_table.add_widget(Label())
        else:
            for i, row in enumerate(data):
                self.add_row(i + 1, row)

    def add_header(self):
        """Add the header row to the leaderboard table."""
        headers = ["#", "Pseudo", "Score", "%"]
        for h in headers:
            self.score_table.add_widget(
                Label(text=h, bold=True, size_hint_y=None, height=40, color=TEAL)
            )

    def add_row(self, rank, row_data):
        """Add a score row to the leaderboard table.

        Args:
            rank (int): Position du joueur.
            row_data (dict): Données du score.
        """
        self.score_table.add_widget(Label(text=str(rank), size_hint_y=None, height=40))
        self.score_table.add_widget(
            Label(text=row_data["pseudo"], size_hint_y=None, height=40)
        )
        self.score_table.add_widget(
            Label(
                text=f"{row_data['score']}/{row_data['goalscore']}",
                size_hint_y=None,
                height=40,
            )
        )
        self.score_table.add_widget(
            Label(text=f"{int(row_data['percent'])}%", size_hint_y=None, height=40)
        )
