import random

class Figurka:
    """
    Reprezentuje jednu figurku na šachovnici.

    Atributy:
    - barva (str): Barva figurky, "o" (hráč) nebo "x" (počítač).
    - dama (bool): Informace, zda je figurka proměněná na dámu.
    """

    def __init__(self, barva):
        """
        Inicializuje figurku.

        Parametry:
        - barva (str): Barva figurky, "o" nebo "x".
        """
        self.barva = barva
        self.dama = False

    def vrat_znak(self):
        """
        Vrátí znak figurky pro výpis na šachovnici.

        Návratová hodnota:
        - str: Malé písmeno pro pěšce, velké písmeno pro dámu.
        """
        if self.dama:
            return self.barva.upper()
        else:
            return self.barva


class Dama:
    """
    Hlavní třída hry Dáma.

    Uchovává stav šachovnice a řídí průběh celé hry.
    """

    def __init__(self):
        """
        Vytvoří instanci hry v počátečním stavu.
        """
        self.sachovnice = []
        self.hra_bezi = True
        self.vytvor_sachovnici()

    def vytvor_sachovnici(self):
        """
        Vytvoří prázdnou šachovnici 8x8 a rozestaví figurky.
        """
        for r in range(8):
            radek = []
            for s in range(8):
                radek.append(None)
            self.sachovnice.append(radek)

        # počítač nahoře
        for r in range(2):
            for s in range(8):
                if (r + s) % 2 == 1:
                    self.sachovnice[r][s] = Figurka("x")

        # hráč dole
        for r in range(6, 8):
            for s in range(8):
                if (r + s) % 2 == 1:
                    self.sachovnice[r][s] = Figurka("o")

    def vypis_sachovnici(self):
        """
        Vypíše aktuální stav šachovnice.
        """
        pismena = ["A","B","C","D","E","F","G","H"]

        print("  1 2 3 4 5 6 7 8")
        for r in range(8):
            print(pismena[r], end=" ")
            for s in range(8):
                if self.sachovnice[r][s] is None:
                    print(".", end=" ")
                else:
                    print(self.sachovnice[r][s].vrat_znak(), end=" ")
            print()
        print()

    def preved_pozici(self, vstup):
        """
        Převede vstupní souřadnici (např. "A3") na indexy.

        Parametry:
        - vstup (str): Souřadnice ve formátu písmeno + číslo.

        Návratová hodnota:
        - tuple[int | None, int | None]:
          Dvojice (řádek, sloupec), při neplatném vstupu (None, None).
        """
        pismena = ["A","B","C","D","E","F","G","H"]

        if len(vstup) != 2:
            return None, None

        x = vstup[0].upper()
        y = vstup[1]

        if x not in pismena:
            return None, None

        if not y.isdigit():
            return None, None

        radek = pismena.index(x)
        sloupec = int(y) - 1

        if sloupec < 0 or sloupec > 7:
            return None, None

        return radek, sloupec
    
    def preved_pozici_nazpet(self, r, s):
        """
        Převede indexy pozice zpět na výstupní formát (např. "A3").

        Parametry:
        - r (int): Index řádku.
        - s (int): Index sloupce.

        Návratová hodnota:
        - tuple[str, str]: (písmeno řádku, číslo sloupce).
        """
        pismena = ["A","B","C","D","E","F","G","H"]
        return pismena[r], str(s + 1)


    def je_v_rozsahu(self, r, s):
        """
        Ověří, že pozice leží na šachovnici.

        Parametry:
        - r (int): Index řádku.
        - s (int): Index sloupce.

        Návratová hodnota:
        - bool: True pokud je pozice v rozsahu 0-7, jinak False.
        """
        return 0 <= r < 8 and 0 <= s < 8

    def ma_figurky(self, barva):
        """
        Zjistí, zda zadaná barva má na šachovnici alespoň jednu figurku.

        Parametry:
        - barva (str): Barva figurky, která se má hledat.

        Návratová hodnota:
        - bool: True pokud figurka dané barvy existuje, jinak False.
        """
        for r in range(8):
            for s in range(8):
                figurka = self.sachovnice[r][s]
                if figurka is not None and figurka.barva == barva:
                    return True
        return False

    # ----------------------------------------------------

    def smery_pesce(self, figurka):
        """
        Vrátí povolené směry pohybu pěšce podle barvy.

        Parametry:
        - figurka (Figurka): Figurka, pro kterou se směry určují.

        Návratová hodnota:
        - list[tuple[int, int]]: Seznam kroků (r, s).
        """
        if figurka.barva == "o":
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]

    def tahy_pesce(self, r, s, figurka):
        """
        Vygeneruje všechny tahy pěšce z dané pozice.

        Parametry:
        - r (int): Výchozí řádek pěšce.
        - s (int): Výchozí sloupec pěšce.
        - figurka (Figurka): Pěšec, pro kterého tahy počítáme.

        Návratová hodnota:
        - list[tuple]: Seznam tahů ve formátu (cil_r, cil_s, je_brani, odebrat).
        """
        tahy = []
        for krok_r, krok_s in self.smery_pesce(figurka):
            dalsi_r = r + krok_r
            dalsi_s = s + krok_s

            if not self.je_v_rozsahu(dalsi_r, dalsi_s):
                continue

            if self.sachovnice[dalsi_r][dalsi_s] is None:
                tahy.append((dalsi_r, dalsi_s, False, None))
                continue

            cil = self.sachovnice[dalsi_r][dalsi_s]
            if cil.barva == figurka.barva:
                continue

            skok_r = dalsi_r + krok_r
            skok_s = dalsi_s + krok_s
            if self.je_v_rozsahu(skok_r, skok_s) and self.sachovnice[skok_r][skok_s] is None:
                tahy.append((skok_r, skok_s, True, (dalsi_r, dalsi_s)))

        return tahy

    def tahy_damy_ve_smeru(self, r, s, krok_r, krok_s, barva):
        """
        Vygeneruje tahy dámy v jednom diagonálním směru.

        Parametry:
        - r (int): Výchozí řádek dámy.
        - s (int): Výchozí sloupec dámy.
        - krok_r (int): Posun řádku v jednom kroku.
        - krok_s (int): Posun sloupce v jednom kroku.
        - barva (str): Barva dámy.

        Návratová hodnota:
        - list[tuple]: Seznam tahů ve formátu (cil_r, cil_s, je_brani, odebrat).
        """
        tahy = []
        dalsi_r = r + krok_r
        dalsi_s = s + krok_s

        while self.je_v_rozsahu(dalsi_r, dalsi_s):
            cil = self.sachovnice[dalsi_r][dalsi_s]

            if cil is None:
                tahy.append((dalsi_r, dalsi_s, False, None))
                dalsi_r += krok_r
                dalsi_s += krok_s
                continue

            if cil.barva == barva:
                return tahy

            skok_r = dalsi_r + krok_r
            skok_s = dalsi_s + krok_s
            while self.je_v_rozsahu(skok_r, skok_s) and self.sachovnice[skok_r][skok_s] is None:
                tahy.append((skok_r, skok_s, True, (dalsi_r, dalsi_s)))
                skok_r += krok_r
                skok_s += krok_s
            return tahy

        return tahy

    def tahy_damy(self, r, s, figurka):
        """
        Vygeneruje všechny tahy dámy z dané pozice.

        Parametry:
        - r (int): Výchozí řádek dámy.
        - s (int): Výchozí sloupec dámy.
        - figurka (Figurka): Dáma, pro kterou tahy počítáme.

        Návratová hodnota:
        - list[tuple]: Seznam tahů ve formátu (cil_r, cil_s, je_brani, odebrat).
        """
        tahy = []
        smery = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for krok_r, krok_s in smery:
            tahy.extend(self.tahy_damy_ve_smeru(r, s, krok_r, krok_s, figurka.barva))

        return tahy

    def mozne_tahy_figurky(self, r, s):
        """
        Vrátí všechny možné tahy figurky na pozici [r, s].

        Parametry:
        - r (int): Řádek figurky.
        - s (int): Sloupec figurky.

        Návratová hodnota:
        - list[tuple]: Seznam tahů ve formátu (cil_r, cil_s, je_brani, odebrat).
        """
        figurka = self.sachovnice[r][s]
        if figurka is None:
            return []

        if figurka.dama:
            return self.tahy_damy(r, s, figurka)
        return self.tahy_pesce(r, s, figurka)

    # ----------------------------------------------------

    def ziskej_vsechny_tahy(self, barva):
        """
        Vrátí všechny platné tahy hráče dané barvy.

        Pokud existuje braní, vrací pouze tahy braní.
        Pokud existuje braní dámou, má přednost před běžným braním pěšcem.

        Parametry:
        - barva (str): Barva hráče ("o" nebo "x").

        Návratová hodnota:
        - list[tuple]: Seznam trojic (r, s, tah), kde tah je ve formátu
          (cil_r, cil_s, je_brani, odebrat).
        """
        normalni = []
        brani = []
        brani_dama = []

        for r in range(8):
            for s in range(8):
                figurka = self.sachovnice[r][s]
                if figurka is not None and figurka.barva == barva:

                    tahy = self.mozne_tahy_figurky(r, s)

                    for tah in tahy:
                        if tah[2] == True:  # je to braní
                            if figurka.dama:
                                brani_dama.append((r,s,tah))
                            else:
                                brani.append((r,s,tah))
                        else:
                            normalni.append((r,s,tah))

        if brani_dama:
            return brani_dama
        if brani:
            return brani
        return normalni

    # ----------------------------------------------------

    def proved_tah(self, r, s, tah):
        """
        Provede jeden tah figurky z pozice [r, s] a vypíše pozici odebrané figurky, pokud braní proběhlo.

        Parametry:
        - r (int): Výchozí řádek figurky.
        - s (int): Výchozí sloupec figurky.
        - tah (tuple): Tah ve formátu (cil_r, cil_s, je_brani, odebrat).

        Návratová hodnota:
        - tuple[int, int]: Nová pozice figurky (řádek, sloupec).
        """
        figurka = self.sachovnice[r][s]
        cil_r = tah[0]
        cil_s = tah[1]

        self.sachovnice[cil_r][cil_s] = figurka
        self.sachovnice[r][s] = None

        # pokud bylo braní
        if tah[2] == True:
            odebrat = tah[3]
            self.sachovnice[odebrat[0]][odebrat[1]] = None
            pismeno, cislo = self.preved_pozici_nazpet(odebrat[0], odebrat[1])
            print(f"Byla odebrána figurka {pismeno}{cislo}")

        # proměna na dámu
        if figurka.barva == "o" and cil_r == 0:
            figurka.dama = True
        if figurka.barva == "x" and cil_r == 7:
            figurka.dama = True

        return cil_r, cil_s

    # ----------------------------------------------------

    def dostupne_tahy_figurky(self, tahy, r, s):
        """
        Vyfiltruje tahy, které patří figurce na pozici [r, s].

        Parametry:
        - tahy (list[tuple]): Seznam všech dostupných tahů hráče.
        - r (int): Řádek vybírané figurky.
        - s (int): Sloupec vybírané figurky.

        Návratová hodnota:
        - list[tuple]: Tahy odpovídající vybrané figurce.
        """
        dostupne = []
        for tah in tahy:
            if tah[0] == r and tah[1] == s:
                dostupne.append(tah)
        return dostupne

    def vypis_tahy(self, tahy):
        """
        Vypíše očíslovaný seznam tahů.

        Parametry:
        - tahy (list[tuple]): Tahy ve formátu (r, s, tah) nebo přímo tahy.

        Návratová hodnota:
        - None
        """
        for i in range(len(tahy)):
            cil = tahy[i][2] if len(tahy[i]) == 3 else tahy[i]
            print(i, "->", chr(cil[0] + 65), cil[1] + 1)

    def nacti_volbu(self, vyzva, maximum):
        """
        Načte od uživatele číslo tahu a ověří rozsah.

        Parametry:
        - vyzva (str): Text výzvy pro vstup.
        - maximum (int): Nejvyšší povolený index.

        Návratová hodnota:
        - int | None: Zvolený index nebo None při neplatném vstupu.
        """
        text = input(vyzva)
        if not text.isdigit():
            print("Neplatná volba.")
            return None

        volba = int(text)
        if volba < 0 or volba > maximum:
            print("Neplatná volba.")
            return None

        return volba

    def vyber_tah_hrace(self, tahy):
        """
        Interaktivně vybere figurku hráče a jeden její tah.

        Parametry:
        - tahy (list[tuple]): Seznam všech platných tahů hráče.

        Návratová hodnota:
        - tuple[int, int, tuple]: Výchozí pozice figurky a vybraný tah.
        """
        while True:
            vstup = input("Vyber figurku (např. A3): ")
            r, s = self.preved_pozici(vstup)
            if r is None:
                print("Neplatná pozice.")
                continue

            if self.sachovnice[r][s] is None:
                print("Na této pozici není žádná figurka.")
                continue

            if self.sachovnice[r][s].barva =="x":
                print("Tohle není tvoje figurka!")
                continue

            dostupne = self.dostupne_tahy_figurky(tahy, r, s)
            if not dostupne:
                print("Tato figurka nemá tah.")
                continue

            print("Možné tahy:")
            self.vypis_tahy(dostupne)
            volba = self.nacti_volbu("Vyber číslo tahu: ", len(dostupne) - 1)
            if volba is None:
                continue

            return r, s, dostupne[volba][2]

    def proved_retezove_brani_hrace(self, r, s):
        """
        Zpracuje povinné pokračování v braní po prvním braní hráče.

        Parametry:
        - r (int): Aktuální řádek figurky.
        - s (int): Aktuální sloupec figurky.

        Návratová hodnota:
        - tuple[int, int]: Konečná pozice figurky po dokončení braní.
        """
        while True:
            dalsi_brani = []
            for tah in self.mozne_tahy_figurky(r, s):
                if tah[2]:
                    dalsi_brani.append(tah)

            if not dalsi_brani:
                return r, s

            print("Musíš pokračovat v braní!")
            self.vypis_tahy(dalsi_brani)
            volba = self.nacti_volbu("Vyber další braní: ", len(dalsi_brani) - 1)
            if volba is None:
                continue

            r, s = self.proved_tah(r, s, dalsi_brani[volba])

    def hrac_tah(self):
        """
        Zpracuje celý tah hráče včetně případného vícenásobného braní.

        Návratová hodnota:
        - bool: True pokud byl tah proveden, False pokud hráč nemá žádný tah.
        """
        tahy = self.ziskej_vsechny_tahy("o")
        if not tahy:
            return False

        r, s, tah = self.vyber_tah_hrace(tahy)
        novy_r, novy_s = self.proved_tah(r, s, tah)

        if tah[2]:
            self.proved_retezove_brani_hrace(novy_r, novy_s)

        return True


    # ----------------------------------------------------

    def pocitac_tah(self):
        """
        Provede tah počítače náhodným výběrem ze všech platných tahů.

        Návratová hodnota:
        - bool: True pokud byl tah proveden, False pokud počítač nemá tah.
        """
        tahy = self.ziskej_vsechny_tahy("x")
        if not tahy:
            return False

        vybrany = random.choice(tahy)

        r = vybrany[0]
        s = vybrany[1]
        tah = vybrany[2]

        novy_r, novy_s = self.proved_tah(r, s, tah)

        # pokračuje jen pokud první tah byl braní
        if tah[2] == True:

            while True:
                dalsi_tahy = self.mozne_tahy_figurky(novy_r, novy_s)

                dalsi_brani = []
                for t in dalsi_tahy:
                    if t[2] == True:
                        dalsi_brani.append(t)

                if not dalsi_brani:
                    break

                dalsi = random.choice(dalsi_brani)
                novy_r, novy_s = self.proved_tah(novy_r, novy_s, dalsi)

        return True

    # ----------------------------------------------------

    def zkontroluj_vyhru(self):
        """
        Zkontroluje, jestli některá strana neztratila všechny figurky.
        """
        hrac = False
        pocitac = False

        for r in range(8):
            for s in range(8):
                figurka = self.sachovnice[r][s]
                if figurka is not None:
                    if figurka.barva == "o":
                        hrac = True
                    if figurka.barva == "x":
                        pocitac = True

        if not hrac:
            print("Vyhrál počítač!")
            self.hra_bezi = False
        if not pocitac:
            print("Vyhrál hráč!")
            self.hra_bezi = False

    # ----------------------------------------------------

    def spust(self):
        """
        Spustí hlavní herní cyklus.
        """
        while self.hra_bezi:

            self.vypis_sachovnici()
            print("Tvůj tah:")
            if not self.hrac_tah():
                if self.ma_figurky("o"):
                    print("Hráč nemá tah. Remíza (pat).")
                else:
                    print("Vyhrál počítač!")
                self.vypis_sachovnici()
                break

            self.zkontroluj_vyhru()

            if not self.hra_bezi:
                break

            self.vypis_sachovnici()
            print("Tah počítače:")
            if not self.pocitac_tah():
                if self.ma_figurky("x"):
                    print("Počítač nemá tah. Remíza (pat).")
                else:
                    print("Vyhrál hráč!")
                self.vypis_sachovnici()    
                break

            self.zkontroluj_vyhru()


# ---------------------------

hra = Dama()
hra.spust()
