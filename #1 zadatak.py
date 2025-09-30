#1. zadatak - knjiga
class Knjiga: 
    def _init_(self, naslov, autor, godina_izdanja):
        self.naslov = naslov
        self.autor = autor
        self.godina_izdanja = godina_izdanja
knjiga1= Knjiga("Hamlet","William Shakespeare",1603)
knjiga2 = Knjiga("Gospodar muha","J.R.R. Tolkien", 1954)

print(f"Naslov: {knjiga1.naslov}, Autor: {knjiga1.autor}, Godina izdavanja: {knjiga1.godina_izdanja}")
print(f"Naslov: {knjiga2.naslov}, Autor: {knjiga2.autor}, Godina izdavanja: {knjiga2.godina_izdanja}")
