from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty


from pathlib import Path


from uikivy import (
    AfficherMenu,
    SubmenuMode,
    SubmenuCont,
    SubmenuQuizzType,
    ShowQuizz,
    ShowLeaderboard,
)  # , ShowGameOver

from kivy.uix.screenmanager import ScreenManager

from engine import Engine
from uikivy import BaseScreen


BASEPATH = Path(__name__).parent


# application principale
class Appli(App):
    """Main application class for GéoQuizz.

    Cette classe centralise l'initialisation de l'application, la création
    du moteur de jeu, la gestion des écrans et les propriétés globales
    partagées entre les différents écrans (pseudo, mode, continent, type
    de quiz).

    Attributes:
        title (str): Titre affiché dans la fenêtre de l'application.
        icon (str): Chemin vers l'icône de l'application.
        pseudo (StringProperty): Nom du joueur utilisé dans le jeu et les scores.
        mode (StringProperty): Mode de jeu sélectionné ('norm' ou 'mar').
        continent (StringProperty): Continent choisi pour filtrer les pays.
        type_quizz (StringProperty): Type de quiz sélectionné ('Capitale', 'Drapeau', 'Tout').
        engine (Engine): Moteur de jeu contenant la logique et les données.
        ui (BaseScreen): Écran de base (non utilisé directement mais conservé pour compatibilité).
        question_ui (ShowQuizz): Instance de l'écran de quiz.
        sm (ScreenManager): Gestionnaire d'écrans de l'application.
    """

    title = "GéoQuizz"
    icon = "images/applogo.ico"

    # variables partagées
    pseudo = StringProperty("Player 1")
    mode = StringProperty(
        "si ca s'affiche c'est que ca marche pas comme il faut"
    )  # marathon / par defaut
    continent = StringProperty("si ca s'affiche c'est que ca marche pas comme il faut")
    type_quizz = StringProperty(
        "si ca s'affiche c'est que ca marche pas comme il faut"
    )  # capitale/flag/tout

    def __init__(self, **kwargs):
        """Initialize the main application class.

        Instancie le moteur de jeu, l'écran de base et l'écran de quiz.
        Prépare les composants internes nécessaires au fonctionnement global
        de l'application.

        Args:
            **kwargs: Arguments transmis à la classe App de Kivy.
        """

        super().__init__()
        self.engine = Engine()
        self.ui = BaseScreen()
        self.question_ui = ShowQuizz()

    def build(self):
        """Build and configure the application's UI.

        Configure la fenêtre (taille, couleur), initialise le ScreenManager
        et enregistre tous les écrans de l'application (menu, sous-menus,
        quiz, classement). Définit l'écran d'accueil comme écran initial.

        Returns:
            ScreenManager: Le gestionnaire d'écrans configuré.
        """

        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        Window.size = (800, 800)
        # Builder.load_file("affichermenu.kv") #ne gere pas path, sert à definir les kivy files à utiliser

        # gestionnaire d'écrans
        self.sm = ScreenManager()
        self.sm.add_widget(AfficherMenu(name="menu"))
        self.sm.add_widget(SubmenuMode(name="smenu_mode"))
        self.sm.add_widget(SubmenuCont(name="smenu_cont"))
        self.sm.add_widget(SubmenuQuizzType(name="smenu_quizz-type"))
        self.sm.add_widget(ShowQuizz(name="show-quizz"))
        # self.sm.add_widget(ShowGameOver(name='show-go'))
        self.sm.add_widget(ShowLeaderboard(name="show-lb"))

        self.sm.current = "menu"

        return self.sm


# démarrage
if __name__ == "__main__":
    Appli().run()
