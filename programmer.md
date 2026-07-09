# Dáma - Programátorská dokumentace

*Autor: Markéta Mokrá*

### Obsah
1. Popis hry
2. Struktura programu 
3. Datové struktury
4. Logika hry
5. Logika počítače
6. Vstup a výstup

## 1. Popis hry 

Program realizuje jednoduchou konzolovou verzi deskové hry dáma na šachovnici 8×8.
Hráč hraje za figurky `o` proti počítači, který ovládá figurky `x`.
Program dodržuje základní pravidla dámy: diagonální pohyb, povinné braní, vícenásobné braní a povýšení na dámu.
Hra probíhá v textovém režimu v terminálu a je ovládána klávesnicí.

## 2. Struktura programu 
Zvolen je objektově orientovaný přístup v Pythonu:

* Třída Figurka reprezentuje jednu figurku na šachovnici (barva a příznak dámy).

* Třída Dama reprezentuje celou hru: obsahuje šachovnici, logiku generování tahů, provádění tahů, kontrolu výhry a hlavní herní cyklus.

Tahy jsou generovány čistě na základě aktuálního stavu šachovnice, bez ukládání historie.

### Třída Figurka
*Třída Figurka reprezentuje jednu figurku na šachovnici.*

* `barva` udává, komu figurka patří.

* `dama` rozeznává obyčejnou figurku od dámy.

* `vrat_znak()` slouží pouze pro výpis – malé písmeno pro pěšce, velké pro dámu.

### Třída Dama
*Třída Dama zapouzdřuje celou logiku hry.*

Obsahuje šachovnici, metody pro generování tahů, provádění tahů, tah hráče, tah počítače a kontrolu konce hry.

## 3. Datové struktury 
### Reprezentace šachovnice

Šachovnice je reprezentována jako 2D seznam 8 řádků, každý řádek je seznam 8 položek:`self.sachovnice[r][s]` 

* Hodnota `None` znamená prázdné pole.
* Instance `Figurka` znamená obsazené pole.

Inicializace probíhá v metodě `vytvor_sachovnici()`:
* nejprve se vytvoří 8×8 `None`
* poté se na pole v horních dvou řadách (0,1) umístí `Figurka("x")`
* na tmavá pole ve spodních dvou řadách (6,7) se umístí `Figurka("o")`

## 4. Logika hry

* Logika hry je rozdělena do několika klíčových funkcí, které spolupracují na tom, aby byl v každém okamžiku k dispozici korektní seznam tahů a aby se partie posouvala dopředu. 

* Metoda `mozne_tahy_figurky(r, s)` na základě pozice a typu figurky (pěšec/dáma) vrací všechny tahy této figurky ve tvaru čtveřic `(cil_r, cil_s, je_brani, odebrat)` – tedy souřadnice cílového pole, informaci, zda jde o braní, a případně souřadnice soupeřovy figurky, která má být při braní odstraněna. 

* Funkce `ziskej_vsechny_tahy(barva)` prochází celou šachovnici, sbírá všechny tahy všech figurek dané barvy a rozdělí je na obyčejné tahy, braní pěšcem a braní dámou; podle toho pak vrací buď jen braní (s preferencí dám), nebo, pokud žádné braní neexistuje, obyčejné tahy. 

* Metoda `proved_tah(r, s, tah)` potom jeden konkrétní tah skutečně provede – přesune figurku na cílové pole, případně odstraní soupeřovu figurku zadanou v poli odebrat a při vstupu na poslední řadu nastaví příznak `dama = True`, čímž z pěšce vytvoří dámu. 

* Na tomo základu stojí funkce `hrac_tah()` a `pocitac_tah()`, které volají `ziskej_vsechny_tahy`, nechají vybrat konkrétní tah a použijí `proved_tah` – včetně případného opakovaného volání při vícenásobném braní. 

* Tento blok funkcí tak tvoří jádro logiky hry: definují, jaké tahy jsou povolené, jak se promítají do stavu šachovnice a jak se střídají tahy hráče a počítače v hlavním cyklu `spust()`.

## 5. Logika počítače

Logika počítače je následující:

1. Počítač si nechá vygenerovat všechny povolené tahy podle aktuálního stavu hry.

2. Pokud nemá žádný tah, vrátí `False` (později se to vyhodnotí jako remíza nebo výhra protivníka).

3. Z aktuálně dostupných tahů náhodně vybere jeden pomocí `random.choice`.

4. Vybraný tah provede metodou `proved_tah`.

5. Pokud šlo o braní, počítač zkusí stejnou figurkou pokračovat v braní:

* vygeneruje všechny možné tahy této figurky,

* z nich vyfiltruje pouze tahy s braním,

* dokud existují, náhodně vybírá jeden z nich a provádí ho.

Důležité je, že inteligence počítače není poziční – nijak nehodnotí, zda je tah „strategicky výhodný“. Jeho logika spočívá pouze v:

* dodržení pravidel hry,

* povinném braní (včetně vícenásobného),

* náhodném výběru mezi povolenými možnostmi.

## 6. Vstup a výstup
### Vstup 

*Program je interaktivní, používá standardní vstup:*

#### Výběr figurky:

* uživatel zadává souřadnici ve formátu písmeno + číslo, např. A3, H6,

* vstup se převádí funkcí `preved_pozici`,

 * neplatné vstupy (špatný formát, mimo rozsah, prázdné pole, figurka bez tahů) jsou odmítnuty a vyžádá se nové zadání.

#### Výběr konkrétního tahu:

* program nejprve vypíše všechny možné cílové pozice pro vybranou figurku očíslované od 0,

* hráč zadá číslo tahu, které se zpracuje funkcí `nacti_volbu`,

* u neplatné volby (nečíslo, číslo mimo rozsah) je zobrazeno chybové hlášení a volba se opakuje.

### Výstup

*Program používá pouze textový výstup:*

* zobrazení šachovnice (`vypis_sachovnici`) – mřížka 8×8, řádky A–H, sloupce 1–8:

* `.` znamená prázdné pole

* `o` / `x` pěšce, `O` / `X` dámu.

#### informativní texty:

* „Tvůj tah:“, „Tah počítače:“

* chybová hlášení typu „Neplatná pozice.“, „Neplatná volba.“, "Na této pozici není žádná figurka.", "Tohle není tvoje figurka!", "Tato figurka nemá tah." 

* informace o povinném pokračování v braní („Musíš pokračovat v braní!“)

* informace o tom, pokud z šachovnice byla odtraněna figurka ("Byla odebrána figurka {pismeno}{cislo}")

#### závěrečná hlášení:

* „Vyhrál hráč!“,

* „Vyhrál počítač!“,

* „Hráč nemá tah. Remíza (pat).“,

* „Počítač nemá tah. Remíza (pat).“.

Výstup je navržen tak, aby si uživatel z textu vždy dokázal rekonstruovat aktuální stav hry a pochopil důvod ukončení partie.
