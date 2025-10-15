# C:\Users\NewHorizon\Documents\PythonProjects\EnglishLearn\venv\Scripts\Activate.ps1
# pip freeze > requirements.txt

from tkinter import *
from tkinter import ttk
from oop_dict import DictionaryGame
from oop_upstairs import UpstairsGame
from time import sleep


class InitialFrame:
    def __init__(self):
        self.root = Tk() 
        self.root.title("Учим Английский (и немного Русский)")
        self.root.geometry("1300x800")

        self.select_game()
    
    def select_game(self):
        self.frame_select_game = ttk.Frame(self.root, borderwidth=1, relief=SOLID, padding=10, height=300)
        self.inform_lbl = ttk.Label(self.frame_select_game, text="ВЫБЕРИ ИГРУ", font=("Arial", 20))
        self.inform_lbl.pack(pady=20)
        self.dict_btn = ttk.Button(self.frame_select_game, text="Словарь", command=self.start_dictionary_game)
        self.dict_btn.pack(fill='both', expand=True)
        self.upstairs_btn = ttk.Button(self.frame_select_game, text="Лесенка", command=self.start_upstairs_game)
        self.upstairs_btn.pack(fill='both', expand=True)
        self.frame_select_game.pack(anchor=NW, fill=X, padx=5, pady=5)

    def start_dictionary_game(self):
        self.frame_select_game.pack_forget()
        self.dictionary_game = DictionaryGame(self.root)

    def start_upstairs_game(self):
        self.frame_select_game.pack_forget()
        self.dictionary_game = UpstairsGame(self.root)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = InitialFrame()
    app.run()
