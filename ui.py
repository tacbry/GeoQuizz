import tkinter as tk
from pathlib import Path
from tkinter import ttk
from PIL import Image, ImageTk

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



def afficher_menu(self):
    #menu = tk.Toplevel(self) #pas ce que je voulais faire mais utile si je veux pop up
    menu_frame = tk.Frame(self, background = BACKGROUND_COLOR)
    menu_frame.pack(pady=10)


    logo = Image.open(BASEPATH / "images" / "applogo.png").resize((200, 200))
    logo = ImageTk.PhotoImage(logo)
    lbl_logo = tk.Label(menu_frame, image = logo, background = BACKGROUND_COLOR, width = 200, height = 200 )
    lbl_logo.pack(padx=10, pady=10)
    lbl_logo.image = logo

    play_button = tk.Button(menu_frame, text = "Play", command = lambda: (afficher_quizz(self).tkraise()))
    play_button.pack(padx=10, pady=10)

    quit_btn = ttk.Button(menu_frame, command= self.quit, text="QUIT")
    quit_btn.pack(side= 'bottom')


    return menu_frame



def afficher_quizz(self):
    quiz_frame = tk.Frame(self)
    quiz_frame.tkraise()

    lbl = tk.Label(quiz_frame, text = "QUIZZE")
    lbl.pack(padx=10, pady=10)

    return quiz_frame




def quizz_capitale(self):
    ...

def quizz_flag(self):
    ...

def afficher_game_over(self):
    game_over_frame = ttk.Frame(self)

    return game_over_frame

def afficher_leaderboard(self):
    score_frame = ttk.Frame(self)

    return score_frame

def main():
    global country_data
    root = tk.Tk()
    root.title("GéoQuizz")
    root.iconbitmap(BASEPATH / "images" / "applogo.ico")
    root.backgroundcolor = BACKGROUND_COLOR
    country_data = engine.load_country_data()
    afficher_menu(self = root)
    root.mainloop()

