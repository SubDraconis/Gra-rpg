import pytest

import funkcje


def test_tworzenie_pola_zwraca_poprawny_typ_terenu():
    mapa = {(0, 0): "W"}

    wynik = funkcje.tworzenie_pola(0, 1, mapa)

    assert wynik in {"L", "W", "R", "M", "E", "J"}
    assert isinstance(wynik, str)


def test_interakcje_wm_wywołuje_mapę_i_wypisuje_wartość(capsys):
    mapa = lambda x, y: "W" if (x, y) == (0, 0) else "."
    wynik = funkcje.interakcje_wm(0, 0, mapa)
    print("wynik =", wynik)
    wyjście = capsys.readouterr().out
    print("wyjście =", wyjście)
    assert wynik is None
    assert "W" in wyjście


def test_interakcje_wm_raises_type_error_when_map_is_dict():
    with pytest.raises(TypeError):
        funkcje.interakcje_wm(0, 0, {(0, 0): "W"})

def test_tworzenie_pola():
    mapa = funkcje.generuj_mape_10x10()
    wynik = funkcje.tworzenie_pola(10, 10, mapa)
    print(wynik)
    assert wynik in {"L", "W", "R", "M", "E", "J"}
    assert isinstance(wynik, str)


def test_generuj_mape_10x10():
    mapa = funkcje.generuj_mape_10x10()
    assert (0, 0) in mapa
    assert len(mapa) == 100
