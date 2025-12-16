import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import xml.etree.ElementTree as ET
from datetime import datetime
 
 
class Dobavljac:
    def __init__(self, dob_id, naziv, kontakt):
        self.dob_id = dob_id
        self.naziv = naziv
        self.kontakt = kontakt
 
    def __str__(self):
        return f"{self.naziv} ({self.kontakt})"
 
 
class Proizvod:
    def __init__(self, naziv, sifra, cijena, kolicina, dobavljac):
        self.naziv = naziv
        self.sifra = sifra
        self.cijena = cijena
        self.kolicina = kolicina
        self.dobavljac = dobavljac
        self.povijest = []  
 
    def promijeni_kolicinu(self, iznos, opis):
        self.kolicina += iznos
        self.povijest.append(f"{datetime.now()}: {opis} ({iznos})")
 
    def kriticno(self):
        return self.kolicina < 5
 
    def to_xml(self):
        raise NotImplementedError()
 
 
class PrehrambeniProizvod(Proizvod):
    def __init__(self, naziv, sifra, cijena, kolicina, dobavljac, rok_trajanja):
        super().__init__(naziv, sifra, cijena, kolicina, dobavljac)
        self.rok_trajanja = rok_trajanja
 
    def istice(self):
        try:
            datum = datetime.strptime(self.rok_trajanja, "%d.%m.%Y")
            return (datum - datetime.now()).days < 5
        except:
            return False
 
    def to_xml(self):
        e = ET.Element("PrehrambeniProizvod")
        ET.SubElement(e, "naziv").text = self.naziv
        ET.SubElement(e, "sifra").text = self.sifra
        ET.SubElement(e, "cijena").text = str(self.cijena)
        ET.SubElement(e, "kolicina").text = str(self.kolicina)
        ET.SubElement(e, "dobavljac").text = str(self.dobavljac.dob_id)
        ET.SubElement(e, "rok").text = self.rok_trajanja
        return e
 
 
class TehnickiProizvod(Proizvod):
    def __init__(self, naziv, sifra, cijena, kolicina, dobavljac, jamstvo):
        super().__init__(naziv, sifra, cijena, kolicina, dobavljac)
        self.jamstvo = jamstvo
 
    def to_xml(self):
        e = ET.Element("TehnickiProizvod")
        ET.SubElement(e, "naziv").text = self.naziv
        ET.SubElement(e, "sifra").text = self.sifra
        ET.SubElement(e, "cijena").text = str(self.cijena)
        ET.SubElement(e, "kolicina").text = str(self.kolicina)
        ET.SubElement(e, "dobavljac").text = str(self.dobavljac.dob_id)
        ET.SubElement(e, "jamstvo").text = str(self.jamstvo)
        return e
 
 
class StockwiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StockWise Lite – Inventar trgovine")
        self.root.geometry("900x600")
 
        self.proizvodi = []
        self.dobavljaci = []
        self.next_dob_id = 1
 
        self.create_menu()
        self.create_ui()
        self.create_status()
 
 
    def create_menu(self):
        meni = tk.Menu(self.root)
 
        file_menu = tk.Menu(meni, tearoff=0)
        file_menu.add_command(label="Spremi XML", command=self.spremi_xml)
        file_menu.add_command(label="Učitaj XML", command=self.ucitaj_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Izlaz", command=self.root.quit)
        meni.add_cascade(label="Datoteka", menu=file_menu)
 
        report_menu = tk.Menu(meni, tearoff=0)
        report_menu.add_command(label="Generiraj izvještaj", command=self.izvjestaj)
        meni.add_cascade(label="Izvještaji", menu=report_menu)
 
        meni.add_command(label="O aplikaciji", command=lambda: messagebox.showinfo("O aplikaciji", "StockWise Lite\nSimulacija inventara trgovine\nAutor: Lukas Černeha"))
        self.root.config(menu=meni)
 
 
    def create_status(self):
        self.status = tk.Label(self.root, text="Spremno", anchor="w")
        self.status.pack(side="bottom", fill="x")
 
 
    def create_ui(self):
        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)
 
        forma = ttk.LabelFrame(main, text="Unos proizvoda")
        forma.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
 
        self.tip_var = tk.StringVar(value="Prehrambeni")
        ttk.Label(forma, text="Tip:").grid(row=0, column=0)
        ttk.OptionMenu(forma, self.tip_var, "Prehrambeni", "Prehrambeni", "Tehnički").grid(row=0, column=1)
 
        self.unos = {}
        polja = ["Naziv", "Šifra", "Cijena", "Količina", "Rok trajanja / Jamstvo"]
        for i, p in enumerate(polja, start=1):
            ttk.Label(forma, text=p).grid(row=i, column=0)
            e = ttk.Entry(forma)
            e.grid(row=i, column=1)
            self.unos[p] = e
 
        ttk.Label(forma, text="Dobavljač:").grid(row=6, column=0)
        self.dob_var = tk.StringVar()
        self.dob_lista = ttk.Combobox(forma, textvariable=self.dob_var, values=[], state="readonly")
        self.dob_lista.grid(row=6, column=1)
 
        ttk.Button(forma, text="Dodaj proizvod", command=self.dodaj_proizvod).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(forma, text="Dodaj dobavljača", command=self.novi_dobavljac).grid(row=8, column=0, columnspan=2)
 
        lista_frame = ttk.LabelFrame(main, text="Inventar")
        lista_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
 
        self.lista = tk.Listbox(lista_frame)
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", self.prikazi_povijest)
 
        pov_frame = ttk.LabelFrame(main, text="Povijest promjena")
        pov_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.pov_text = tk.Text(pov_frame, width=30)
        self.pov_text.pack(fill="both", expand=True)
 
        update = ttk.LabelFrame(main, text="Prodaja / Nabava")
        update.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
 
        self.kol_var = tk.StringVar()
        ttk.Entry(update, textvariable=self.kol_var).pack(side="left", padx=5)
        ttk.Button(update, text="Prodaj", command=lambda: self.promjena(-1)).pack(side="left", padx=5)
        ttk.Button(update, text="Nabava", command=lambda: self.promjena(1)).pack(side="left", padx=5)
 
    def osvjezi_listu(self):
        self.lista.delete(0, tk.END)
        for p in self.proizvodi:
            tekst = f"{p.naziv} ({p.kolicina} kom)"
            if p.kriticno():
                tekst += " !!! "
            self.lista.insert(tk.END, tekst)
 
    def novi_dobavljac(self):
        win = tk.Toplevel(self.root)
        win.title("Novi dobavljač")
        tk.Label(win, text="Naziv:").grid(row=0, column=0)
        tk.Label(win, text="Kontakt:").grid(row=1, column=0)
        naz = tk.Entry(win)
        kon = tk.Entry(win)
        naz.grid(row=0, column=1)
        kon.grid(row=1, column=1)
 
        def spremi():
            d = Dobavljac(self.next_dob_id, naz.get(), kon.get())
            self.next_dob_id += 1
            self.dobavljaci.append(d)
            self.dob_lista["values"] = [str(x) for x in self.dobavljaci]
            win.destroy()
 
        tk.Button(win, text="Spremi", command=spremi).grid(row=2, column=0, columnspan=2)
 
    def dodaj_proizvod(self):
        try:
            tip = self.tip_var.get()
            naziv = self.unos["Naziv"].get()
            sifra = self.unos["Šifra"].get()
            cijena = float(self.unos["Cijena"].get())
            kolicina = int(self.unos["Količina"].get())
            dodatno = self.unos["Rok trajanja / Jamstvo"].get()
            dob_naz = self.dob_var.get()
 
            dob = next((d for d in self.dobavljaci if str(d) == dob_naz), None)
            if not dob:
                raise ValueError("Odaberite dobavljača.")
 
            if tip == "Prehrambeni":
                p = PrehrambeniProizvod(naziv, sifra, cijena, kolicina, dob, dodatno)
            else:
                p = TehnickiProizvod(naziv, sifra, cijena, kolicina, dob, int(dodatno))
 
            self.proizvodi.append(p)
            self.osvjezi_listu()
            self.status.config(text="Proizvod dodan.")
 
        except Exception as e:
            messagebox.showerror("Greška", str(e))
 
    def prikazi_povijest(self, event):
        sel = self.lista.curselection()
        if not sel: return
        p = self.proizvodi[sel[0]]
        self.pov_text.delete("1.0", tk.END)
        for linija in p.povijest:
            self.pov_text.insert(tk.END, linija + "\n")
 
    def promjena(self, smjer):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Greška", "Odaberite proizvod.")
            return
        try:
            iznos = int(self.kol_var.get()) * smjer
            p = self.proizvodi[sel[0]]
            p.promijeni_kolicinu(iznos, "Prodaja" if smjer == -1 else "Nabava")
            self.osvjezi_listu()
            self.prikazi_povijest(None)
            self.status.config(text="Stanje ažurirano.")
        except:
            messagebox.showerror("Greška", "Unesite ispravan broj.")
 
 
    def spremi_xml(self):
        fn = filedialog.asksaveasfilename(defaultextension=".xml")
        if not fn: return
 
        root = ET.Element("Inventar")
 
        dob_el = ET.SubElement(root, "Dobavljaci")
        for d in self.dobavljaci:
            e = ET.SubElement(dob_el, "Dobavljac")
            ET.SubElement(e, "id").text = str(d.dob_id)
            ET.SubElement(e, "naziv").text = d.naziv
            ET.SubElement(e, "kontakt").text = d.kontakt
 
        proizvodi_el = ET.SubElement(root, "Proizvodi")
        for p in self.proizvodi:
            proizvodi_el.append(p.to_xml())
 
        tree = ET.ElementTree(root)
        tree.write(fn, encoding="utf-8", xml_declaration=True)
        self.status.config(text="XML spremljen.")
 
    def ucitaj_xml(self):
        fn = filedialog.askopenfilename()
        if not fn: return
        try:
            tree = ET.parse(fn)
            root = tree.getroot()
 
            self.dobavljaci.clear()
            for d in root.find("Dobavljaci"):
                dob = Dobavljac(int(d.find("id").text), d.find("naziv").text, d.find("kontakt").text)
                self.dobavljaci.append(dob)
 
            self.proizvodi.clear()
            for p in root.find("Proizvodi"):
                naziv = p.find("naziv").text
                sifra = p.find("sifra").text
                cijena = float(p.find("cijena").text)
                kolicina = int(p.find("kolicina").text)
                dob_id = int(p.find("dobavljac").text)
                dob = next(x for x in self.dobavljaci if x.dob_id == dob_id)
 
                if p.tag == "PrehrambeniProizvod":
                    rok = p.find("rok").text
                    obj = PrehrambeniProizvod(naziv, sifra, cijena, kolicina, dob, rok)
                else:
                    jamstvo = int(p.find("jamstvo").text)
                    obj = TehnickiProizvod(naziv, sifra, cijena, kolicina, dob, jamstvo)
 
                self.proizvodi.append(obj)
 
            self.dob_lista["values"] = [str(x) for x in self.dobavljaci]
            self.osvjezi_listu()
            self.status.config(text="XML učitan.")
 
        except Exception as e:
            messagebox.showerror("Greška", str(e))
 
 
    def izvjestaj(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt")
        if not fn: return
 
        with open(fn, "w", encoding="utf-8") as f:
            f.write("IZVJEŠTAJ INVENTARA\n\n")
            for p in self.proizvodi:
                f.write(f"{p.naziv}: {p.kolicina} kom – dobavljač: {p.dobavljac.naziv}\n")
 
        self.status.config(text="Izvještaj generiran.")
 
 
root = tk.Tk()
app = StockwiseApp(root)
root.mainloop()
 