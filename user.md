# Uživatelská dokumentace

## Dáma

* Autor: Markéta Mokrá 

### Obsah

1. Popis hry

2. Požadavky a spuštění

3. Návod k použití

### 1. Popis hry
Program je klasická desková hra dáma na šachovnici 8×8.
Hráč hraje s figurkami `o` proti počítači, který ovládá figurky `x`.
Cílem hry je vyhodit všechny soupeřovy figurky nebo ho dostat do stavu, kdy už nemá žádný platný tah.
Pěšci se pohybují diagonálně dopředu a po dosažení poslední řady se mění na dámu, která se může pohybovat o libovolný počet polí diagonálně.
Hra probíhá v terminálu a hráč ji ovládá pomocí klávesnice.

### 2. Požadavky a spuštění

* Prostředí: Python 3.x 

* Knihovny: Program používá pouze standardní knihovnu random. 

* Spuštění: Program spustíte v terminálu příkazem: `python Dama.py`

### 3. Návod k použití
Po spuštění programu se vytvoří šachovnice 8×8, nahoře jsou figurky počítače `x`, dole figurky hráče `o`.

Šachovnice se vypisuje jako mřížka, řádky jsou označeny písmeny A–H a sloupce čísly 1–8.

Hráč je na tahu jako první. Program vypíše text `Tvůj tah:` a čeká na zadání tahu.

Tah se zadává ve dvou krocích:

1. Nejprve musíte zadat souřadnici své figurky ve formátu písmeno + číslo (například A3) a potvrdit Enterem.

2. Pokud má daná figurka alespoň jeden platný tah, program vypíše očíslovaný seznam všech možných cílových polí a vyzve hráče, aby zadal číslo vybraného tahu.

Pokud zadá neplatný vstup (neexistující pole, pole bez vlastní figurky, figurka bez tahů, číslo mimo rozsah), program vypíše chybové hlášení a vyzve hráče k novému zadání.

Pokud tah zahrnuje braní, figurka přeskočí soupeřovu figurku, tato figurka je z desky odstraněna a program vypíše jaká figurka byla odstraněna. 

Jestliže po prvním braní existuje možnost dalšího braní stejnou figurkou, program hráče donutí v braní pokračovat, dokud jsou k dispozici další tahy s braním.

Po dokončení tahu program zkontroluje, zda některá strana neztratila všechny figurky:

 - pokud hráč nemá žádnou figurku, vypíše se `Vyhrál počítač!`

 - pokud počítač nemá žádnou figurku, vypíše se `Vyhrál hráč!`

 - pokud některá strana má figurky, ale nemá žádný platný tah, partie končí remízou (pat).
