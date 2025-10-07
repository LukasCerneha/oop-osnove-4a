import tkinter as tk
from tkinter import messagebox

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} {self.razred}"
    
class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")

        self.ucenici = []       
        self.odabrani_ucenik_index = None       
        self.create_widgets()
     def create_widgets(self):    

        self.frame = tk.Frame(self.root)