import random
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from matplotlib.figure import Figure

# podstawowe ustawienia dla okna
root = tk.Tk()
root.title("Aplikacja do generowania wykresów")
root.geometry("950x585")
root.resizable(False, False)

# Logika tworzenia wykresu
class Wykres:
    KOLORY = ["blue", "red", "green", "purple", "orange", "black"]

    def __init__(self):
        self.fig = Figure(figsize=(6.5, 4.5))
        self.ax = self.fig.add_subplot()

    def generuj_wykres(self, serie_danych, typ, kolor, grubosc, tytul, osX, osY, siatka):
        self.ax.clear()
        self.ax.set_aspect("auto")
        szerokosc_miedzy_slupkami = 0.25
        licznik_narysowanych_slupkow = 0

        pozostale_kolory = [c for c in self.KOLORY if c != kolor]

        for indeks, seria in enumerate(serie_danych):
            nazwa_wykresu = f'Wykres{indeks + 1}'
            etykiety_osi_X = [x + 1 + licznik_narysowanych_slupkow * szerokosc_miedzy_slupkami for x in range(len(seria))]

            # k to jest kolor aktualnego wykresu
            if indeks == 0:
                k = kolor
            else:
                # jeśli kolory do wyboru dla innych wykresów się skończą to uzupełniamy je na nowo
                if len(pozostale_kolory) == 0:
                    pozostale_kolory = [c for c in self.KOLORY if c != kolor]
                # kolory dla pozostałych wykresów
                k = pozostale_kolory.pop(0)  # wyjmij pierwszy z brzegu kolor
            if typ == "liniowy":
                # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html
                self.ax.plot(
                    etykiety_osi_X,
                    seria,
                    color=k,
                    marker="o",
                    linewidth=grubosc,
                    label=nazwa_wykresu
                )
            elif typ == "slupkowy":
                self.ax.bar(
                    etykiety_osi_X,
                    seria,
                    width=szerokosc_miedzy_slupkami,
                    color=k,
                    label=nazwa_wykresu
                )
                licznik_narysowanych_slupkow += 1
            elif typ == "kolowy":
                self.ax.pie(seria, labels=seria, autopct="%.2f%%")
                break

        self.ax.set_title(tytul)
        if typ != "kolowy":
            self.ax.set_xlabel(osX)
            self.ax.set_ylabel(osY)

        self.ax.grid(siatka)

        if typ != "kolowy" and serie_danych:
            self.ax.legend(loc="upper right")

    def zapisz(self, sciezka):
        self.fig.savefig(sciezka)


# frontend
class Aplikacja:
    def __init__(self):
        self.wykres = Wykres()
        self.dane_z_przycisku_jako_lista = []

        # Najpierw dzielimy okno na dwie ramy
        self.panel_lewy = tk.Frame(root, padx=10, pady=5)
        self.panel_prawy = tk.Frame(root, padx=10, pady=5, bg="orange")
        self.panel_lewy.grid(row=0, column=0)
        self.panel_prawy.grid(row=0, column=1)

        # Miejsce na wykres
        self.etykieta_wykres_img = tk.Label(self.panel_prawy)
        self.etykieta_wykres_img.grid(row=0, column=1)

        numer_wiersza = 0
        self.etykieta_pole_danych = tk.Label(self.panel_lewy, text="Dane (serie rozdziel znakiem ;):")
        self.etykieta_pole_danych.grid(row=numer_wiersza, column=0, pady=5)
        numer_wiersza += 1

        # przy tworzeniu pola Entry na dane, ustawiamy wartości domyślne
        dane_startowe = "10, 20, 30, 40; 5, 15, 25, 35"
        self.pole_danych = tk.Entry(self.panel_lewy, width=30)
        self.pole_danych.insert(0, dane_startowe)
        self.pole_danych.grid(row=numer_wiersza, column=0, pady=2)
        numer_wiersza += 1

        tk.Label(self.panel_lewy, text="W pliku słupki poprzedź nagłówkiem.").grid(row=numer_wiersza, column=0)
        numer_wiersza += 1
        self.przycisk_wczytaj_dane = tk.Button(
            self.panel_lewy,
            text="Wczytaj plik (.csv, .xlsx, .txt)",
            command=self.wczytaj_dane_z_pliku
        )
        self.przycisk_wczytaj_dane.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        # Przycisk LOSUJ DANE
        self.przycisk_losuj_dane = tk.Button(self.panel_lewy, text="Losuj dane", command=self.losuj)
        self.przycisk_losuj_dane.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        # Wybór typu wykresu
        tk.Label(self.panel_lewy, text="Typ wykresu: ").grid(row=numer_wiersza, column=0, pady=5)
        numer_wiersza += 1

        self.typ = tk.StringVar(value="liniowy")
        for opcja in ["liniowy", "slupkowy", "kolowy"]:
            tk.Radiobutton(
                self.panel_lewy,
                text=opcja.capitalize(),
                value=opcja,
                variable=self.typ
            ).grid(row=numer_wiersza, column=0)
            numer_wiersza += 1

        tk.Label(self.panel_lewy, text="Kolor głównego wykresu: ").grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        # Menu wyboru koloru
        self.kolor = tk.StringVar(value=self.wykres.KOLORY[0])
        self.menu = tk.OptionMenu(self.panel_lewy, self.kolor, *self.wykres.KOLORY)

        self.menu.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        tk.Label(self.panel_lewy, text="Grubość każdej linii:").grid(row=numer_wiersza, column=0)
        numer_wiersza += 1
        self.grubosc_linii = tk.IntVar(value=2)
        tk.Scale(self.panel_lewy, from_=1, to=10, orient="horizontal", variable=self.grubosc_linii).grid(row=numer_wiersza, column=0, sticky="we")
        numer_wiersza += 1

        tk.Label(self.panel_lewy, text="Tytuł / Osie X i Y:").grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        self.tytul = tk.Entry(self.panel_lewy)
        self.tytul.insert(0, "Wykres porównawczy")
        self.osX = tk.Entry(self.panel_lewy)
        self.osX.insert(0, "Punkty pomiarowe")
        self.osY = tk.Entry(self.panel_lewy)
        self.osY.insert(0, "Wartości")

        self.tytul.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1
        self.osX.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1
        self.osY.grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        self.siatka = tk.BooleanVar(value=True)
        tk.Checkbutton(self.panel_lewy, variable=self.siatka, text="Siatka").grid(row=numer_wiersza, column=0)
        numer_wiersza += 1

        self.generuj_przycisk = tk.Button(
            self.panel_lewy,
            text="Generuj wykres",
            bg="#fab123",
            command=self.wyslij_dane_do_narysowania_wykresu,


        )
        self.generuj_przycisk.grid(row=numer_wiersza, column=0, pady=5, padx=5)
        numer_wiersza += 1

        tk.Button(
            self.panel_lewy,
            text="ZAPISZ WYKRES...",
            command=self.zapisz,
            fg="blue"
        ).grid(row=numer_wiersza, column=0, sticky="ew")
        numer_wiersza += 1

        self.wyslij_dane_do_narysowania_wykresu()

        self.exit_button = tk.Button(
            self.panel_lewy,
            text="ZAKOŃCZ PROGRAM",
            command=self.zamknij_aplikacje,
            bg="red",
            pady=5
        )
        self.exit_button.grid(row=numer_wiersza, column=0)

    def zamknij_aplikacje(self):
        root.destroy()

    def zapisz(self):
        sciezka = filedialog.asksaveasfilename(
            initialfile="wygenerowany_wykres",
            defaultextension=".png",
            filetypes=[
                ("Obraz PNG", "*.png"),
                ("Obraz JPG", "*.jpg"),
                ("dokument gotowy do druku (PDF)", "*.pdf"),
                ("plik grafiki wektorowej (SVG)", "*.svg"),
            ]
        )
        if sciezka:
            self.wykres.zapisz(sciezka)
            messagebox.showinfo(title="Komunikat", message="Plik z wykresem został zapisany pomyślnie.")

    def wyslij_dane_do_narysowania_wykresu(self):
        self.przekonwertuj_pole_danych_na_liczby()
        self.wykres.generuj_wykres(
            self.dane_z_przycisku_jako_lista,
            self.typ.get(),
            self.kolor.get(),
            self.grubosc_linii.get(),
            self.tytul.get(),
            self.osX.get(),
            self.osY.get(),
            self.siatka.get()
        )

        self.wykres.zapisz("aktualny_wykres.png")
        self.obraz = tk.PhotoImage(file="aktualny_wykres.png")
        self.etykieta_wykres_img.config(image=self.obraz)

    def losuj(self):
        ile_wykresow = random.randint(1, 3)
        serie = [] # [[],[]] (lista list)
        for x in range(ile_wykresow):
            dane_do_wykresu = []
            ile_liczb = random.randint(1, 5)
            for x in range(ile_liczb):
                liczba = random.randint(0, 50)
                dane_do_wykresu.append(liczba)
            serie.append(dane_do_wykresu)

        serie_napis = "; ".join([", ".join(map(str, seria)) for seria in serie])

        self.pole_danych.delete(0, tk.END)
        self.pole_danych.insert(0, serie_napis)
        self.wyslij_dane_do_narysowania_wykresu()

    def wczytaj_dane_z_pliku(self):
        sciezka = filedialog.askopenfilename(
            filetypes=[("Arkusz excela", ".xlsx"), ("Zwykły plik tekstowy", ".txt"), ("Plik csv", ".csv")]
        )

        if not sciezka:
            return

        try:
            if sciezka.endswith(".xlsx"):
                tabela_danych_z_pliku = pd.read_excel(sciezka)
            else:
                tabela_danych_z_pliku = pd.read_csv(sciezka)

            print(f'tabela_danych_z_pliku.columns = {tabela_danych_z_pliku.columns}') # 'coerce' wymusza konwersje danych
            dane_po_konwersji_na_liczby = [pd.to_numeric(tabela_danych_z_pliku[nazwa_kolumny], errors="coerce").dropna().tolist() for nazwa_kolumny in tabela_danych_z_pliku.columns]
            print(dane_po_konwersji_na_liczby)
            tekst = " ; ".join([",".join(map(str, seria)) for seria in dane_po_konwersji_na_liczby])
            self.pole_danych.delete(0, tk.END)
            self.pole_danych.insert(0, tekst)
            self.wyslij_dane_do_narysowania_wykresu()
        except Exception as e:
            messagebox.showerror("Błąd", f'Nie odczytano pliku o nazwie {e}')

    def przekonwertuj_pole_danych_na_liczby(self):
        try:
            cale_dane_tekstowo = self.pole_danych.get()
            self.dane_z_przycisku_jako_lista = [
                [float(wartosc) for wartosc in seria.split(',')] for seria in cale_dane_tekstowo.split(';')
            ]
        except ValueError:
            messagebox.showerror("Błąd", "Dane liczbowe wpisz po przecinku. Serię danych oddzielaj znakiem średnika.")


Aplikacja()
root.mainloop()