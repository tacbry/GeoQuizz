from kivy.core.window import Window
from kivy.lang import Builder

from engine import *
from uikivy import *

from kivy.uix.screenmanager import ScreenManager


BASEPATH = Path(__name__).parent


#application principale


class Appli(App):
    title = "GéoQuizz"
    icon = 'images/applogo.ico'
    Window.clearcolor = (0.15, 0.15, 0.15, 1)


    def build(self):
        root = StackLayout(orientation='tb-lr')

        #Builder.load_file("affichermenu.kv") #ne gere pas path

        #gestionnaire d'écrans
        sm = ScreenManager()
        sm.add_widget(AfficherMenu(name='menu'))
        sm.add_widget(SubmenuMode(name='smenu_mode'))
        sm.add_widget(SubmenuCont(name='smenu_cont'))


        sm.current = 'menu'

        root.add_widget(sm)

        return root





#démarrage
if __name__ == "__main__":
    Appli().run()