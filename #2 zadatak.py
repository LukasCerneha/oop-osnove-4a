class BankovniRacun:
    def __init__(self,ime_prezime, broj_racuna):
        self.ime_prezime = ime_prezime
        self.broj_racuna = broj_racuna
        self.stanje = 0.0

    def uplati (self, iznos):
        if iznos > 0:
            self.stanje += iznos
            print(f"uplata od {iznos:.2f} EUR na račun {self.broj_racuna} je uspješan")
        else:
            print("Neispravan iznos za uplatu. Iznos mora biti pozitivan")
    
    def isplati (self, iznos):
        if iznos <=0:
            print("Greška: iznos za isplatu mora biti pozitivan")
        elif self.stanje >= iznos:
            self.stanje -= iznos 
            print(f"Isplata od {iznos:.2f} EUR uspješna. Novo stanje: {self.stanje:.2f} EU")
        else: 
            print(f"Isplata nije moguća. Iznos mora biti manji od stanja računa. (Stanje {self.stanje:.2f}EUR.)")
    def info(self):
        print("-" * 25)
        print(f"Vlasnik: {self.ime_vlasnika}")
        print(f"Broj računa: {self.broj_racuna}")
        print(f"Stanje: {self.stanje:.2f} EUR")
        print("-" * 25)
        