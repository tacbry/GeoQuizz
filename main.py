from kivy.app import App
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty


from pathlib import Path


from uikivy import AfficherMenu, SubmenuMode, SubmenuCont, SubmenuQuizzType, ShowQuizz, ShowLeaderboard#, ShowGameOver

from kivy.uix.screenmanager import ScreenManager

from engine import Engine
from uikivy import BaseScreen


BASEPATH = Path(__name__).parent


#application principale
class Appli(App):
    title = "GéoQuizz"
    icon = 'images/applogo.ico'



    #variables partagées
    pseudo  =StringProperty("Player 1")
    mode = StringProperty("si ca s'affiche c'est que ca marche pas comme il faut")#marathon / par defaut
    continent = StringProperty("si ca s'affiche c'est que ca marche pas comme il faut")
    type_quizz = StringProperty("si ca s'affiche c'est que ca marche pas comme il faut") #capitale/flag/tout

    def __init__(self, **kwargs):
        super().__init__()
        self.engine = Engine()
        self.ui = BaseScreen()
        self.question_ui = ShowQuizz()

    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        Window.size = (800, 800)
        #Builder.load_file("affichermenu.kv") #ne gere pas path, sert à definir les kivy files à utiliser

        #gestionnaire d'écrans
        self.sm = ScreenManager()
        self.sm.add_widget(AfficherMenu(name='menu'))
        self.sm.add_widget(SubmenuMode(name='smenu_mode'))
        self.sm.add_widget(SubmenuCont(name='smenu_cont'))
        self.sm.add_widget(SubmenuQuizzType(name='smenu_quizz-type'))
        self.sm.add_widget(ShowQuizz(name='show-quizz'))
        #self.sm.add_widget(ShowGameOver(name='show-go'))
        self.sm.add_widget(ShowLeaderboard(name='show-lb'))


        self.sm.current = 'menu'

        return self.sm

#démarrage
if __name__ == "__main__":
    Appli().run()