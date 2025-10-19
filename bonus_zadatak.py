import tkinter as tk
from tkinter import messagebox
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
 
 
class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred
 
    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"
 
 
class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija učenika")
        self.root.geometry("600x450")
        self.ucenici = []
        self.odabrani_ucenik_index = None
 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
 
        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")
 
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)
 
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, sticky="W", padx=5, pady=5)
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, sticky="EW", padx=5, pady=5)
 
        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, sticky="W", padx=5, pady=5)
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, sticky="EW", padx=5, pady=5)
 
        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, sticky="W", padx=5, pady=5)
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, sticky="EW", padx=5, pady=5)
 
        unos_frame.columnconfigure(1, weight=1)
 
        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10, sticky="EW")
 
        self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="EW")
 
        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)
 
        gumbi_frame = tk.Frame(self.root, pady=10)
        gumbi_frame.grid(row=2, column=0, sticky="EW")
        gumbi_frame.columnconfigure((0, 1, 2, 3), weight=1)
 
        self.spremi_csv_gumb = tk.Button(gumbi_frame, text="Spremi CSV", command=self.spremi_u_csv)
        self.spremi_csv_gumb.grid(row=0, column=0, padx=5, sticky="EW")
 
        self.ucitaj_csv_gumb = tk.Button(gumbi_frame, text="Učitaj CSV", command=self.ucitaj_iz_csv)
        self.ucitaj_csv_gumb.grid(row=0, column=1, padx=5, sticky="EW")
 
        self.spremi_xml_gumb = tk.Button(gumbi_frame, text="Spremi XML", command=self.spremi_u_xml)
        self.spremi_xml_gumb.grid(row=0, column=2, padx=5, sticky="EW")
 
        self.ucitaj_xml_gumb = tk.Button(gumbi_frame, text="Učitaj XML", command=self.ucitaj_iz_xml)
        self.ucitaj_xml_gumb.grid(row=0, column=3, padx=5, sticky="EW")
 
    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
 
        if not ime or not prezime or not razred:
            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")
            return
 
        novi_ucenik = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi_ucenik)
        self.osvjezi_prikaz()
        self.ocisti_polja()
 
    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))
 
    def ocisti_polja(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)
 
    def odaberi_ucenika(self, event):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return
        self.odabrani_ucenik_index = odabrani_indeksi[0]
        ucenik = self.ucenici[self.odabrani_ucenik_index]
        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, ucenik.ime)
        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, ucenik.prezime)
        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, ucenik.razred)
 
    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is None:
            messagebox.showwarning("Upozorenje", "Niste odabrali učenika.")
            return
 
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
 
        if not ime or not prezime or not razred:
            messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")
            return
 
        ucenik = self.ucenici[self.odabrani_ucenik_index]
        ucenik.ime = ime
        ucenik.prezime = prezime
        ucenik.razred = razred
 
        self.osvjezi_prikaz()
        self.ocisti_polja()
        self.odabrani_ucenik_index = None
 
    def spremi_u_csv(self):
        if not self.ucenici:
            messagebox.showinfo("Info", "Nema učenika za spremiti.")
            return
        try:
            with open("ucenici.csv", "w", newline='', encoding="utf-8") as f:
                polja = ['ime', 'prezime', 'razred']
                writer = csv.DictWriter(f, fieldnames=polja)
                writer.writeheader()
                for u in self.ucenici:
                    writer.writerow({'ime': u.ime, 'prezime': u.prezime, 'razred': u.razred})
            messagebox.showinfo("Uspjeh", "Učenici su spremljeni u 'ucenici.csv'.")
        except Exception as e:
            messagebox.showerror("Greška", f"Spremanje CSV nije uspjelo:\n{e}")
 
    def ucitaj_iz_csv(self):
        try:
            with open("ucenici.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                nova_lista = []
                for red in reader:
                    ime = red['ime']
                    prezime = red['prezime']
                    razred = red['razred']
                    nova_lista.append(Ucenik(ime, prezime, razred))
            self.ucenici = nova_lista
            self.osvjezi_prikaz()
            self.ocisti_polja()
            messagebox.showinfo("Uspjeh", "Učenici su učitani iz 'ucenici.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka 'ucenici.csv' nije pronađena.")
        except Exception as e:
            messagebox.showerror("Greška", f"Učitavanje CSV nije uspjelo:\n{e}")
 
    def spremi_u_xml(self):
        if not self.ucenici:
            messagebox.showinfo("Info", "Nema učenika za spremiti.")
            return
        try:
            root = ET.Element("ucenici")
            for u in self.ucenici:
                ucenik_el = ET.SubElement(root, "ucenik")
                ET.SubElement(ucenik_el, "ime").text = u.ime
                ET.SubElement(ucenik_el, "prezime").text = u.prezime
                ET.SubElement(ucenik_el, "razred").text = u.razred
 
            xml_string = ET.tostring(root, encoding='utf-8')
            dom = minidom.parseString(xml_string)
            lijepi_xml = dom.toprettyxml(indent="  ")
 
            with open("ucenici.xml", "w", encoding="utf-8") as f:
                f.write(lijepi_xml)
 
            messagebox.showinfo("Uspjeh", "Učenici su spremljeni u 'ucenici.xml'.")
        except Exception as e:
            messagebox.showerror("Greška", f"Spremanje XML nije uspjelo:\n{e}")
 
    def ucitaj_iz_xml(self):
        try:
            tree = ET.parse("ucenici.xml")
            root = tree.getroot()
            nova_lista = []
            for ucenik_el in root.findall("ucenik"):
                ime = ucenik_el.find("ime").text
                prezime = ucenik_el.find("prezime").text
                razred = ucenik_el.find("razred").text
                nova_lista.append(Ucenik(ime, prezime, razred))
 
            self.ucenici = nova_lista
            self.osvjezi_prikaz()
            self.ocisti_polja()
            messagebox.showinfo("Uspjeh", "Učenici su učitani iz 'ucenici.xml'.")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka 'ucenici.xml' nije pronađena.")
        except Exception as e:
            messagebox.showerror("Greška", f"Učitavanje XML nije uspjelo:\n{e}")
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
