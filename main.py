import sys, random
import funkcje
import classy

x, y = 0, 0
Mapa = {
    (0, 0): "W" 
}
mapa_d = {
    (0,0): "E"
}

slownik = {
    "W": "w wiosce",
    "R": "obok rzeki",
    "L": "w lesie",
    "M": "w mieście",
    "E": "przed wejściem do dungeonu",
    "J": "przed jeziorem"
}
opcje = [
    "1 - Poruszyć się na wschód.",
    "2 - Poruszyć się na południe.",
    "3 - Poruszyć się na zachód.",
    "4 - Poruszyć się na północ.",
    "5 - Otwórz ekwipunek / Zmiana sprzętu.",
    "6 - Zobacz profil i statystyki gracza."
]

gracz = funkcje.start()

while True:
    Mapa[(x, y)] = funkcje.tworzenie_pola(x, y, Mapa)
    funkcje.wyswietl_mape(Mapa, x, y)
    print(f"Jesteś {slownik[Mapa[x, y]]} (HP: {gracz.aktualne_hp}/{gracz.max_hp})")
    
  
    if random.randint(1, 10) <= 3:
        funkcje.losuj_wydarzenie(Mapa[x, y], classy.baza_wydarzen, gracz)

    if gracz.aktualne_hp <= 0:
        print("\n☠️ STRACIŁEŚ PRZYTOMNOŚĆ! Miejscowi wieśniacy odnaleźli Cię i odnieśli do wioski.")
        x, y = 0, 0
        gracz.aktualne_hp = gracz.max_hp
        print("Odnawiasz siły i budzisz się w bezpiecznej wiosce...\n")

    print("\nOpcje:")
    for opcja in opcje:
        print(opcja)
    wybor = input("Co chcesz zrobić? ")

    if wybor == "1":
        x += 1
    elif wybor == "2":
        y -= 1
    elif wybor == "3":
        x -= 1
    elif wybor == "4":
        y += 1
    elif wybor == "5":
        funkcje.zarzadzaj_ekwipunkiem(gracz)
    elif wybor == "6":
        gracz.pokaz_status()
    elif Mapa[(x, y)]=="E" and wybor == 7:
        pass
    else:
        print("Nie ma takiej opcji!")