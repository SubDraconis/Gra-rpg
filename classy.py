from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Przedmiot:
    nazwa: str
    typ: str  # "broń", "pancerz", "amulet"
    bonusy: Dict[str, int]  # np. {"Siła": 5, "HP": 20}

@dataclass
class Postac:
    imie: str
    nazwisko: str
    klasa: str
    lv: int = 1
    bazy_statystyki: Dict[str, int] = field(default_factory=lambda: {
        "HP": 100, 
        "Siła": 10, 
        "Zręczność": 10, 
        "Inteligencja": 10
    })
    aktualne_hp: int = 100
    ubrane: Dict[str, Optional[Przedmiot]] = field(default_factory=lambda: {
        "broń": None,
        "pancerz": None,
        "amulet": None
    })
    ekwipunek: List[Przedmiot] = field(default_factory=list)

    @property
    def max_hp(self) -> int:
        """Oblicza maksymalne HP uwzględniając bonusy ze sprzętu."""
        return self.statystyki.get("HP", 100)

    @property
    def statystyki(self) -> Dict[str, int]:
        """Oblicza aktualne statystyki postaci wraz z założonym sprzętem."""
        stats = self.bazy_statystyki.copy()
        for slot, przedmiot in self.ubrane.items():
            if przedmiot:
                for stat, bonus in przedmiot.bonusy.items():
                    stats[stat] = stats.get(stat, 0) + bonus
        return stats

    def zmien_hp(self, ilosc: int):
        """Modyfikuje HP postaci (leczenie/obrażenia)."""
        self.aktualne_hp += ilosc
        if self.aktualne_hp > self.max_hp:
            self.aktualne_hp = self.max_hp
        
        if ilosc < 0:
            print(f"💔 Straciłeś {-ilosc} HP! (Aktualne HP: {self.aktualne_hp}/{self.max_hp})")
        elif ilosc > 0:
            print(f"💚 Odzyskałeś {ilosc} HP! (Aktualne HP: {self.aktualne_hp}/{self.max_hp})")

    def zaloz_przedmiot(self, przedmiot: Przedmiot):
        if przedmiot.typ not in self.ubrane:
            print(f"Nie można założyć przedmiotu typu '{przedmiot.typ}'.")
            return

        if przedmiot in self.ekwipunek:
            self.ekwipunek.remove(przedmiot)

        if self.ubrane[przedmiot.typ] is not None:
            stary_przedmiot = self.ubrane[przedmiot.typ]
            self.ekwipunek.append(stary_przedmiot)
            print(f"Zdjęto: {stary_przedmiot.nazwa}")

        self.ubrane[przedmiot.typ] = przedmiot
        print(f"Założono: {przedmiot.nazwa}")

    def zdejmij_przedmiot(self, typ_slotu: str):
        if typ_slotu in self.ubrane and self.ubrane[typ_slotu] is not None:
            przedmiot = self.ubrane[typ_slotu]
            self.ubrane[typ_slotu] = None
            self.ekwipunek.append(przedmiot)
            print(f"Zdjęto {przedmiot.nazwa} do ekwipunku.")
        else:
            print("Nic tu nie jest założone.")

    def pokaz_status(self):
        print(f"\n================ POSTAĆ: {self.imie} {self.nazwisko} ================")
        print(f"Klasa: {self.klasa} | Poziom: {self.lv}")
        print(f"Życie: {self.aktualne_hp} / {self.max_hp} HP")
        print("--- STATYSTYKI ---")
        for stat, wartosc in self.statystyki.items():
            baza = self.bazy_statystyki.get(stat, 0)
            roznica = wartosc - baza
            bonus_str = f" (+{roznica})" if roznica > 0 else (f" ({roznica})" if roznica < 0 else "")
            print(f"  {stat}: {wartosc}{bonus_str}")
        
        print("--- ZAŁOŻONY SPRZĘT ---")
        for slot, p in self.ubrane.items():
            nazwa_p = p.nazwa if p else "Brak"
            print(f"  {slot.capitalize()}: {nazwa_p}")
        print("========================================================\n")


@dataclass
class Opcja:
    nazwa: str
    opis: str
    wynik_tekst: str
    zmiana_hp: int = 0
    zmiana_statow: Dict[str, int] = field(default_factory=dict)
    nowy_przedmiot: Optional[Przedmiot] = None

@dataclass
class Wydarzenie:
    id: int
    miejsce: str  # "L", "W", "R", "M", "E", "J"
    nazwa: str
    opis: str
    opcje: Dict[str, Opcja]


# ================= BAZA WYDARZEŃ =================
baza_wydarzen = [
    # --- LAS (L) ---
    Wydarzenie(
        id=1, miejsce="L", nazwa="Tajemniczy las",
        opis="Mijasz gęste krzaki i słyszysz podejrzany hałas.",
        opcje={
            "a": Opcja("Sprawdź hałas", "Zagłębiasz się w krzaki...", "Zostałeś zaatakowany przez dzika!", zmiana_hp=-15),
            "b": Opcja("Ignoruj", "Omijasz krzaki szerokim łukiem.", "Bezpiecznie idziesz dalej.")
        }
    ),
    Wydarzenie(
        id=2, miejsce="L", nazwa="Stary Pustelnik",
        opis="Napotykasz starca siedzącego przy ognisku.",
        opcje={
            "a": Opcja("Zaoferuj pomoc", "Dzielisz się zapasami ze starcem.", "Starzec uczy cię skupienia (+2 Inteligencja).", zmiana_statow={"Inteligencja": 2}),
            "b": Opcja("Poproś o broń", "Pustelnik daje ci starą, ale solidną laskę.", "Otrzymujesz nową broń!", nowy_przedmiot=Przedmiot("Dębowa Laska", "broń", {"Siła": 3, "Inteligencja": 2}))
        }
    ),
    Wydarzenie(
        id=3, miejsce="L", nazwa="Gniazdo Dzikich Pszczół",
        opis="Z gałęzi drzewa zwisa ogromne gniazdo pełne miodu.",
        opcje={
            "a": Opcja("Próbuj zdobyć miód", "Wspinasz się na drzewo...", "Pszczoły cię pokąsały, ale zdobyłeś leczniczy miód!", zmiana_hp=-10, nowy_przedmiot=Przedmiot("Amulet Pszczelego Miodu", "amulet", {"HP": 15})),
            "b": Opcja("Odejdź", "Nie ryzykujesz ukąszeń.", "Spokojnie kontynuujesz podróż.")
        }
    ),
    Wydarzenie(
        id=4, miejsce="L", nazwa="Zaklęte Źródło",
        opis="Widzisz krystalicznie czyste, świecące źródło wody.",
        opcje={
            "a": Opcja("Napij się wody", "Pijesz zimną, chłodną wodę.", "Cujesz jak twoje rany się goją!", zmiana_hp=30),
            "b": Opcja("Przemyj twarz", "Przemywasz oczy czystą wodą.", "Twoje zmysły się wyostrzają (+1 Zręczność).", zmiana_statow={"Zręczność": 1})
        }
    ),

    # --- WIOSKA (W) ---
    Wydarzenie(
        id=5, miejsce="W", nazwa="Lokalny Kowal",
        opis="Kowal szuka kogoś do pomocy przy przedmuchiwaniu pieca.",
        opcje={
            "a": Opcja("Pomóż kowalowi", "Pracujesz ciężko przez kilka godzin.", "Młotkowanie wzmocniło twoje mięśnie! (+2 Siła)", zmiana_statow={"Siła": 2}),
            "b": Opcja("Poproś o pancerz", "Kowal daje ci zapasowe skórzane karwasze.", "Otrzymujesz element pancerza!", nowy_przedmiot=Przedmiot("Wzmocnione Karwasze", "pancerz", {"HP": 15}))
        }
    ),
    Wydarzenie(
        id=6, miejsce="W", nazwa="Wiejski Festyn",
        opis="Mieszkańcy wioski świętują zbiory. Zapraszają cię do stołu.",
        opcje={
            "a": Opcja("Dołącz do uczty", "Jesz pyszne pieczenie i pijesz miód.", "Jesteś pełen energii!", zmiana_hp=25),
            "b": Opcja("Weź udział w siłowaniu", "Stajesz do walki na rękę z miejscowym osiłkiem.", "Wgrywasz i zyskujesz uznanie (+1 Siła)!", zmiana_statow={"Siła": 1})
        }
    ),

    # --- RZEKA (R) ---
    Wydarzenie(
        id=7, miejsce="R", nazwa="Zatopiony Wóz",
        opis="W płytkiej wodzie dostrzegasz rozbity kupiecki wóz.",
        opcje={
            "a": Opcja("Przeszukaj wóz", "Wchodzisz do zimnej wody...", "Znajdujesz starożytny amulet na dnie!", nowy_przedmiot=Przedmiot("Amulet Rzecznego Wodnika", "amulet", {"Inteligencja": 3, "HP": 10})),
            "b": Opcja("Idź brzegiem", "Bystry nurt wygląda niebezpiecznie.", "Nic się nie dzieje.")
        }
    ),
    Wydarzenie(
        id=8, miejsce="R", nazwa="Bystry Nurt",
        opis="Chcesz przeprawić się na drugą stronę, ale rzeka jest rwąca.",
        opcje={
            "a": Opcja("Płyń wpław", "Nurt porwał cię i uderzyłeś o kamienie!", "Prawie utonąłeś!", zmiana_hp=-25),
            "b": Opcja("Poszukaj mostu", "Po godzinie znajdujesz bezpieczną kładkę.", "Zyskujesz doświadczenie w nawigacji (+1 Zręczność).", zmiana_statow={"Zręczność": 1})
        }
    ),

    # --- MIASTO (M) ---
    Wydarzenie(
        id=9, miejsce="M", nazwa="Gildia Treningowa",
        opis="Mijasz otwartą bramę miejskiej akademii wojskowej.",
        opcje={
            "a": Opcja("Kup lekcję szermierki", "Trener pokazuje ci zaawansowane pchnięcia.", "Twoja zręczność rośnie! (+2 Zręczność)", zmiana_statow={"Zręczność": 2}),
            "b": Opcja("Medytuj z magami", "Spędzasz czas w cichej bibliotece.", "Odkrywasz sekrety magii! (+2 Inteligencja)", zmiana_statow={"Inteligencja": 2})
        }
    ),
    Wydarzenie(
        id=10, miejsce="M", nazwa="Mroczna Uliczka",
        opis="Z cienia wyłania się zamaskowany zbir z nożem!",
        opcje={
            "a": Opcja("Walcz", "Dochodzi do szybkiej szamotaniny.", "Odpędzasz zbira, ale odnosisz rany.", zmiana_hp=-20),
            "b": Opcja("Uciekaj", "Sprintem wybiegasz na główny plac.", "Uciekasz, ale ćwiczysz kondycję (+1 Zręczność).", zmiana_statow={"Zręczność": 1})
        }
    ),

    # --- DUNGEON / WEJŚCIE (E) ---
    Wydarzenie(
        id=11, miejsce="E", nazwa="Obozowisko Poszukiwaczy",
        opis="Przed wejściem do lochów stacjonuje grupa doświadczonych najemników.",
        opcje={
            "a": Opcja("Odpocznij przy ich ogniu", "Regenerujesz siły przed wejściem.", "Odpoczynek dobrze ci zrobił.", zmiana_hp=40),
            "b": Opcja("Kup używany sprzęt", "Handlujesz z jednym z najemników.", "Otrzymujesz Solidny Talerz Pancerza!", nowy_przedmiot=Przedmiot("Zbroja Najemnika", "pancerz", {"HP": 30, "Siła": 2}))
        }
    ),
    Wydarzenie(
        id=12, miejsce="E", nazwa="Mroczny Ołtarz",
        opis="Stoisz przed starożytnym ołtarzem spowitym czarną mgłą.",
        opcje={
            "a": Opcja("Złóż ofiarę z krwi", "Nacinasz dłoń na kamieniu...", "Tracisz zdrowie, ale otrzymujesz ogromną moc! (-20 HP, +4 Siła)", zmiana_hp=-20, zmiana_statow={"Siła": 4}),
            "b": Opcja("Zniszcz ołtarz", "Rozbijasz przeklęty kamień.", "Mroczna klątwa cię razi!", zmiana_hp=-15)
        }
    ),

    # --- JEZIORO (J) ---
    Wydarzenie(
        id=13, miejsce="J", nazwa="Stary Wędkarz",
        opis="Nad brzegiem jeziora siedzi staruszek z wędką.",
        opcje={
            "a": Opcja("Wspólnie łówcie", "Spędzasz spokojne popołudnie na łowieniu.", "Zjadłeś pyszne ryby i wyciszyłeś umysł.", zmiana_hp=20, zmiana_statow={"Inteligencja": 1}),
            "b": Opcja("Wyciągnij coś z wody", "Wędkarz wyciąga starą skrzynię i daje ci jej zawartość.", "Wyciągasz lśniący Amulet!", nowy_przedmiot=Przedmiot("Amulet Głębin", "amulet", {"HP": 20, "Inteligencja": 2}))
        }
    )
]