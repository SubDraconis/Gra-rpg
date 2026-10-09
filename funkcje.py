import random
import time
from typing import List, Optional
from classy import Opcja, Wydarzenie, Postac, Przedmiot

def tworzenie_pola(x, y, mapa):
    if (x, y) in mapa:
        return mapa[(x, y)]

    kierunki = {
        "Północ": (x, y + 1),
        "Południe": (x, y - 1),
        "Wschód": (x + 1, y),
        "Zachód": (x - 1, y),
        "Północny Wschód": (x + 1, y + 1),
        "Północny Zachód": (x - 1, y + 1),
        "Południowy Wschód": (x + 1, y - 1),
        "Południowy Zachód": (x - 1, y - 1)
    }
    wagi = {
        "L": 50,
        "W": 10,
        "R": 50,
        "M": 15,
        "E": 5,
        "J": 10
    }
    znalezione_pola = {}
    mozliwe_pole = ["L", "W", "J"]

    for nazwa_kierunku, wspolrzedne in kierunki.items():
        if wspolrzedne in mapa:
            znalezione_pola[nazwa_kierunku] = mapa[wspolrzedne]

    sasiednie_pola = list(znalezione_pola.values())

    if any(pole == "R" for pole in sasiednie_pola) or any(pole == "J" for pole in sasiednie_pola):
        mozliwe_pole.append("R")

    if any(pole == "R" for pole in sasiednie_pola) and not any(pole == "M" for pole in sasiednie_pola):
        mozliwe_pole.append("M")
        
    if not any(pole == "E" for pole in sasiednie_pola):
        mozliwe_pole.append("E")
        
    if any(pole == "J" for pole in sasiednie_pola) or any(pole == "R" for pole in sasiednie_pola):
        mozliwe_pole.append("J")

    wagi_mozliwych = [wagi.get(klocek, 10) for klocek in mozliwe_pole]
    return random.choices(mozliwe_pole, weights=wagi_mozliwych, k=1)[0]

def wyswietl_mape(mapa, x_gracza, y_gracza):
    if not mapa:
        print("Mapa jest pusta.")
        return

    x_values = [x for x, _ in mapa]
    y_values = [y for _, y in mapa]

    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    print("Legenda: X=twoja pozycja, W=wioska, L=las, R=rzeka, M=miasto, E=wejście, J=jezioro, .=nieodkryte")

    for y in range(max_y, min_y - 1, -1):
        wiersz = []
        for x in range(min_x, max_x + 1):
            if (x, y) == (x_gracza, y_gracza):
                wiersz.append("X")
            else:
                wiersz.append(mapa.get((x, y), "."))
        print(" ".join(wiersz))

    print()


def generuj_mape_10x10(x_gracza=0, y_gracza=0):
    """Tworzy mapę 10x10 w zakresie x i y od -5 do 4.
    Pozycja gracza jest wpisana jako "W".
    """
    mapa = {}
    for y in range(-5, 5):
        for x in range(-5, 5):
            if x == x_gracza and y == y_gracza:
                mapa[(x, y)] = "W"
            else:
                mapa[(x, y)] = tworzenie_pola(x, y, mapa)
    return mapa

def losuj_wydarzenie(pozycja_gracza: str, baza_wydarzen: List[Wydarzenie], gracz: Postac):
    dostepne = [w for w in baza_wydarzen if w.miejsce == pozycja_gracza]
    
    if not dostepne:
        return
    
    wylosowane = random.choice(dostepne)
    
    print(f"\n⚡ === [WYDARZENIE: {wylosowane.nazwa}] === ⚡")
    print(f"{wylosowane.opis}\n")
    print("MASZ DO WYBORU:")
    
    for litera, opcja in wylosowane.opcje.items():
        print(f" [{litera}] {opcja.nazwa}: {opcja.opis}")
    
    wybor = input("Co wybierasz (a/b)? ").lower().strip()
    
    if wybor in wylosowane.opcje:
        wybrana_opcja = wylosowane.opcje[wybor]
        print(f"\n> {wybrana_opcja.wynik_tekst}")
        time.sleep(1)

        
        if wybrana_opcja.zmiana_hp != 0:
            gracz.zmien_hp(wybrana_opcja.zmiana_hp)

        
        if wybrana_opcja.zmiana_statow:
            for stat, wartosc in wybrana_opcja.zmiana_statow.items():
                gracz.bazy_statystyki[stat] = gracz.bazy_statystyki.get(stat, 0) + wartosc
                znak = "+" if wartosc > 0 else ""
                print(f"✨ Twoja statystyka {stat} zmieniła się o: {znak}{wartosc}")

        
        if wybrana_opcja.nowy_przedmiot:
            gracz.ekwipunek.append(wybrana_opcja.nowy_przedmiot)
            print(f"🎁 Zdobyłeś nowy przedmiot: {wybrana_opcja.nowy_przedmiot.nazwa} ({wybrana_opcja.nowy_przedmiot.typ})!")
            
        time.sleep(1.5)

def zarzadzaj_ekwipunkiem(gracz: Postac):
    while True:
        print("\n=== MENU EKWIPUNKU ===")
        print("1 - Pokaż status postaci i założony sprzęt")
        print("2 - Załóż przedmiot z ekwipunku")
        print("3 - Zdejmij przedmiot")
        print("4 - Powrót do gry")
        
        wybor = input("Wybierz opcję: ")
        
        if wybor == "1":
            gracz.pokaz_status()
        elif wybor == "2":
            if not gracz.ekwipunek:
                print("Twój ekwipunek jest pusty!")
                continue
            print("\nTwój ekwipunek:")
            for i, przedmiot in enumerate(gracz.ekwipunek, start=1):
                bonusy = ", ".join([f"{k}: +{v}" for k, v in przedmiot.bonusy.items()])
                print(f" [{i}] {przedmiot.nazwa} ({przedmiot.typ}) - [{bonusy}]")
            
            try:
                nr = int(input("Wybierz numer przedmiotu do założenia (0 aby anulować): "))
                if 1 <= nr <= len(gracz.ekwipunek):
                    przedmiot_do_zalozenia = gracz.ekwipunek[nr - 1]
                    gracz.zaloz_przedmiot(przedmiot_do_zalozenia)
            except ValueError:
                print("Niepoprawny numer.")
        elif wybor == "3":
            print("\nCo chcesz zdjąć?")
            print("1 - Broń")
            print("2 - Pancerz")
            print("3 - Amulet")
            
            mapa_slotow = {"1": "broń", "2": "pancerz", "3": "amulet"}
            wybor_slotu = input("Wybierz slot (1-3): ")
            if wybor_slotu in mapa_slotow:
                gracz.zdejmij_przedmiot(mapa_slotow[wybor_slotu])
            else:
                print("Nieprawidłowy wybór.")
        elif wybor == "4":
            break

def start() -> Postac:
    dane_klas = {
        "Wojownik": {
            "opis": "Mistrz broni białej i ciężkiego pancerza.",
            "stats": {"HP": 130, "Siła": 15, "Zręczność": 8, "Inteligencja": 5},
            "przedmioty": [
                Przedmiot("Miecz Stalowy", "broń", {"Siła": 6}),
                Przedmiot("Zbroja Płytowa", "pancerz", {"HP": 35}),
                Przedmiot("Amulet Odwagi", "amulet", {"Siła": 2, "HP": 10})
            ]
        },
        "Mag": {
            "opis": "Włada potężną magią żywiołów.",
            "stats": {"HP": 80, "Siła": 5, "Zręczność": 8, "Inteligencja": 18},
            "przedmioty": [
                Przedmiot("Różdżka Żywiołów", "broń", {"Inteligencja": 8}),
                Przedmiot("Jedwabne Szaty", "pancerz", {"HP": 15, "Inteligencja": 4}),
                Przedmiot("Amulet Mądrości", "amulet", {"Inteligencja": 5})
            ]
        },
        "Łotrzyk": {
            "opis": "Mistrz skradania i szybkich ataków.",
            "stats": {"HP": 95, "Siła": 8, "Zręczność": 16, "Inteligencja": 8},
            "przedmioty": [
                Przedmiot("Podwójne Sztylety", "broń", {"Zręczność": 7}),
                Przedmiot("Skórzana Zbroja", "pancerz", {"HP": 20, "Zręczność": 3}),
                Przedmiot("Amulet Cienia", "amulet", {"Zręczność": 4})
            ]
        },
        "Kapłan": {
            "opis": "Specjalizuje się w leczeniu i wspieraniu.",
            "stats": {"HP": 100, "Siła": 7, "Zręczność": 7, "Inteligencja": 15},
            "przedmioty": [
                Przedmiot("Święty Kostur", "broń", {"Inteligencja": 5, "HP": 10}),
                Przedmiot("Szata Kapłańska", "pancerz", {"HP": 25}),
                Przedmiot("Amulet Światła", "amulet", {"Inteligencja": 3, "HP": 15})
            ]
        },
        "Łowca": {
            "opis": "Wyśmienity łucznik i tropiciel.",
            "stats": {"HP": 105, "Siła": 10, "Zręczność": 15, "Inteligencja": 7},
            "przedmioty": [
                Przedmiot("Długi Łuk Cisowy", "broń", {"Zręczność": 6}),
                Przedmiot("Płaszcz Tropiciela", "pancerz", {"HP": 20, "Zręczność": 2}),
                Przedmiot("Amulet Oko Sokoła", "amulet", {"Zręczność": 3})
            ]
        },
        "Paladyn": {
            "opis": "Święty rycerz łączący walkę w zwarciu z magią.",
            "stats": {"HP": 125, "Siła": 13, "Zręczność": 7, "Inteligencja": 10},
            "przedmioty": [
                Przedmiot("Młot Bojowy", "broń", {"Siła": 5}),
                Przedmiot("Pancerz Światłości", "pancerz", {"HP": 30}),
                Przedmiot("Święty Medalion", "amulet", {"HP": 15, "Siła": 2})
            ]
        },
        "Barbarzyńca": {
            "opis": "Dziki wojownik wpadający w bojowy szał.",
            "stats": {"HP": 140, "Siła": 17, "Zręczność": 9, "Inteligencja": 4},
            "przedmioty": [
                Przedmiot("Topór Dwuręczny", "broń", {"Siła": 8}),
                Przedmiot("Skóry Niedźwiedzia", "pancerz", {"HP": 25}),
                Przedmiot("Amulet Dzikiej Krwi", "amulet", {"Siła": 4})
            ]
        },
        "Czarnoksiężnik": {
            "opis": "Czerpie moc z mrocznych paktów i klątw.",
            "stats": {"HP": 85, "Siła": 6, "Zręczność": 7, "Inteligencja": 17},
            "przedmioty": [
                Przedmiot("Mroczna Księga", "broń", {"Inteligencja": 7}),
                Przedmiot("Szaty Paktu", "pancerz", {"HP": 15, "Inteligencja": 3}),
                Przedmiot("Amulet Mrocznej Duszy", "amulet", {"Inteligencja": 4})
            ]
        },
        "Mnich": {
            "opis": "Mistrz sztuk walki i unikania ciosów.",
            "stats": {"HP": 110, "Siła": 11, "Zręczność": 14, "Inteligencja": 8},
            "przedmioty": [
                Przedmiot("Owijki Chi", "broń", {"Siła": 4, "Zręczność": 4}),
                Przedmiot("Szata Klasztorna", "pancerz", {"HP": 20, "Zręczność": 2}),
                Przedmiot("Koraliki Medytacyjne", "amulet", {"Zręczność": 3, "HP": 10})
            ]
        },
        "Nekromanta": {
            "opis": "Mroczny władca śmierci przywołujący nieumarłych.",
            "stats": {"HP": 85, "Siła": 5, "Zręczność": 7, "Inteligencja": 18},
            "przedmioty": [
                Przedmiot("Kostur Czaszki", "broń", {"Inteligencja": 8}),
                Przedmiot("Szata Śmierci", "pancerz", {"HP": 15}),
                Przedmiot("Amulet Kości", "amulet", {"Inteligencja": 4})
            ]
        }
    }
    
    print("=== TWORZENIE POSTACI ===")
    print("Wybierz klasę:")
    for nazwa_klasy, info in dane_klas.items():
        print(f"- {nazwa_klasy}: {info['opis']}")

    wybrana_klasa = ""
    while True:
        wybrana = input("\nNapisz nazwę, aby wybrać klasę: ").strip()
        for k in dane_klas:
            if wybrana.lower() == k.lower():
                wybrana_klasa = k
                break
        if wybrana_klasa:
            break
        print("Nie znaleziono takiej klasy, spróbuj ponownie.")

    print(f"\nWybrano klasę: {wybrana_klasa}")
    imie = input("Napisz swoje imię: ").strip()
    nazwisko = input("Napisz swoje nazwisko: ").strip()

    info_klasy = dane_klas[wybrana_klasa]
    
    gracz = Postac(
        imie=imie,
        nazwisko=nazwisko,
        klasa=wybrana_klasa,
        lv=1,
        bazy_statystyki=info_klasy["stats"].copy(),
        ekwipunek=[]
    )

    print(f"\nOtrzymujesz startowe wyposażenie dla klasy {wybrana_klasa}:")
    for item in info_klasy["przedmioty"]:
        gracz.zaloz_przedmiot(item)

    # Ustawienie poczatkowego HP po założeniu przedmiotów
    gracz.aktualne_hp = gracz.max_hp

    print(f"\nWitaj {gracz.imie} {gracz.nazwisko}! Twoja przygoda się rozpoczyna.\n")
    return gracz

def interakcje_wm(x, y, mapa):
    if isinstance(mapa, dict):
        raise TypeError("mapa musi być funkcją, nie słownikiem współrzędnych")

    if not callable(mapa):
        raise TypeError("mapa musi być funkcją")

    teren = mapa(x, y)

    opcje_terenu = {
        "W": {
            1: "Odwiedź kowala",
            2: "Zajrzyj do karczmy",
            3: "Kup zapasy",
            4: "Sprawdź rynek"
        },
        "L": {
            1: "Zbierz drewno",
            2: "Poluj na zwierzęta",
            3: "Poszukaj schowanego skarbu",
            4: "Odpocznij przy ognisku"
        },
        "R": {
            1: "Udaj się nad rzekę",
            2: "Poszukaj mostu",
            3: "Złap ryby",
            4: "Zbadaj brzeg"
        },
        "M": {
            1: "Idź do gildii",
            2: "Odwiedź sklep",
            3: "Zajrzyj do tawerny",
            4: "Sprawdź forum łowców"
        },
        "E": {
            1: "Wejdź do lochów",
            2: "Rozejrzyj się przy wejściu",
            3: "Porozmawiaj z najemnikami",
            4: "Przygotuj się do bitwy"
        },
        "J": {
            1: "Zbadaj brzeg jeziora",
            2: "Złap rybę",
            3: "Poszukaj ukrytej łodzi",
            4: "Usiądź i odpocznij"
        },
        ".": {
            1: "Sprawdź okolicę",
            2: "Poszukaj śladów",
            3: "Odtwórz trasę"
        }
    }

    print(f"Jesteś w miejscu: {teren}")
    for numer, opis in opcje_terenu.get(teren, {}).items():
        print(f"[{numer}] {opis}")

    return None

