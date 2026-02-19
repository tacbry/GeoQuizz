from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty

from engine import *
from uikivy import *

from kivy.uix.screenmanager import ScreenManager


BASEPATH = Path(__name__).parent


#application principale


class Appli(App):
    title = "GéoQuizz"
    icon = 'images/applogo.ico'

    #variables partagées
    pseudo  =StringProperty("Joueur 1")
    mode = StringProperty("si ca s'affiche c'est que ca marche pas comme il faut")



    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        Window.size = (800, 1000)
        #Builder.load_file("affichermenu.kv") #ne gere pas path

        #gestionnaire d'écrans
        self.sm = ScreenManager()
        self.sm.add_widget(AfficherMenu(name='menu'))
        self.sm.add_widget(SubmenuMode(name='smenu_mode'))
        self.sm.add_widget(SubmenuCont(name='smenu_cont'))

        self.sm.current = 'menu'

        return self.sm





#démarrage
if __name__ == "__main__":
    Appli().run()