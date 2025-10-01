import tkinter as tk

lista_imena = []

def klik_na_gumb():
    ime = unos_imena.get()
    lista_imena.append(ime)
    pozdravna = f""
    for ime in lista_imena:
        pozdravna = pozdravna + f"\nPozdrav {ime}!"
        pozdrav.config(text=pozdravna)
prozor = tk.Tk()
prozor.title("Moj prvi GUI program")
prozor.geometry("500x500")

pozdravna_poruka = tk.Label(prozor, text="Pozdrav 4.a!")
pozdravna_poruka.pack()

uputa = tk.Label(prozor, text="Upiši svoje ime")
uputa.pack()

unos_imena=tk.Entry(prozor)
unos_imena.pack()

gumb = tk.Button(prozor, text="Kliknite me!", command=klik_na_gumb)
gumb.pack()

pozdrav = tk.Label(prozor, text="")
pozdrav.pack()

prozor.mainloop()