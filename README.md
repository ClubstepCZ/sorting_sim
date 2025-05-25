# Simulátor řadicích algoritmů

*Simulátor řadicích algoritmů* je aplikace vytvořená jako součást bakalářské práce. Algoritmy jsou implementovány v jazyce *C*, zatímco samotná simulace – průběh řazení, odhad složitostí a správa algoritmů – je napsána v jazyce *Python* s využitím knihovny *PyQt*.

## Požadavky
Tato sekce popisuje potřebné požadavky pro spuštění aplikace. Mezi hlavní požadavky patří:

- `gcc` s podporou standardu `-std=c11`,
- `python` verze `3.10` a vyšší (**pro jinou verzi je potřeba upravit skript** `run.sh`),
- volitelná distribuce `Linux` (testováno na `Ubuntu` a `Debian`), nebo `macOS`,
- textové editory `vim` a `VS Code` (sloužící k editaci řadicích algoritmů).

## Využití prostředí *venv*

Uživatelské testování poukázalo na chyby v případě nevyužití prostředí `venv`. Tyto problémy byly nejspíše způsobeny konflikty mezi verzemi knihoven v systému a knihovnami vyžadovanými touto aplikací. Proto je silně doporučeno jej používat. V případě jiné verze Pythonu použijte odpovídající název (`python3.11`, `python3`, ...)

### Vytvoření prostředí
```
python3.10 -m venv nazev_prostredi
```

### Aktivace prostředí
```
source nazev_prostredi/bin/activate
```


## Instalace závislostí
Pro spuštění aplikace je potřeba stáhnout závislosti:
```
pip install -r requirements.txt
```

### Obsah souboru *requirements.txt*
```
PySide6>=6.5
matplotlib>=3.5
numpy>=1.21
scikit-learn>=1.0
```

## Spuštění aplikace
Tato sekce popisuje zajištění prostředků pro spuštění aplikace.
Pro spuštění je nezbytná úprava práv skriptu `run.sh`:
```
chmod +x run.sh
```
Následně je možné aplikaci spustit pomocí skriptu:
```
./run.sh
```

### Obsah souboru *run.sh*
```
#!/bin/bash
if [ ! -f "ui_form.py" ]; then
    if command -v pyside6-uic &> /dev/null; then
        pyside6-uic form.ui -o ui_form.py
    else
        python3.10 -m PySide6.scripts.uic form.ui -o ui_form.py
    fi

    if [ ! -f "ui_form.py" ]; then
        exit 1
    fi
fi

python3.10 mainwindow.py
```

V případě jiné verze Pythonu upravte řádky obsahující text `python3.10` podle potřeby.

## Grafické uživatelské rozhraní
Tato sekce popisuje grafické uživatelské rozhraní aplikace a jeho prvky s popisem funkce.

### Selekce algoritmů
Selekce algoritmů je možná v levé části okna, kde je předpřipraveno z několika řadicích algoritmů:
- `Bubble Sort`,
- `Heap Sort`,
- `Insertion Sort`,
- `Merge Sort`,
- `Quick Sort`,
- `Selection Sort`.
- atd..

Algoritmus je zvolen kliknutím na příslušné tlačítko.

### Editace algoritmů
K editaci algoritmů slouží tlačítko `Edit`, které otevře zdrojový kód zvoleného algoritmu v externím textovém editoru. Aplikace podporuje editory `vim` a `VS Code`, které otevřou příslušný adresář daného algoritmu (např. src/bubble_sort).

### Překlad algoritmu
Překlad algoritmu může proběhnout manuálně s využitím příkazu `make` v příslušném adresáři algoritmu:
```
cd src/bubble_sort
make
```
nebo s využitím tlačítka `Make` uvnitř aplikace.

V případě chyby při překladu je chyba hlášena aplikací. Při prvním spuštění aplikace je potřeba algoritmy vždy přeložit.

### Přidání nového algoritmu
Pro přidání nového algoritmu je v horní části aplikace dostupné *textové pole* společně s tlačítkem `Add`.
Zvolený název může mít maximální délku 20 znaků, nesmí začínat číslicí, může používat pouze znaky povolené v názvech souborů a adresářů, včetně mezer a zvolený název se nesmí shodovat s již existujícím algoritmem.
Společně s tím vzniká adresářová struktura a příslušné soubory:
```
/src/
|-- novy_algoritmus/
    |-- novy_algoritmus.c
    |-- Makefile
```
Předchystaný soubor `.c` zahrnuje deklaraci vstupní funkce, která je generická pro veškerou sadu řadicích algoritmů.

### Mazání existujícího algoritmu
Pro mazání algoritmu je k dispozici tlačítko `Delete`, které se váže na aktuálně zvolený algoritmus. Pro korektní smazání je využíváno dvojího ověření, kde je potřeba opět zadat název zvoleného algoritmu.

### Odhad časové a prostorové složitosti
Tlačítko `Determine Complexity` slouží ke spuštění experimentální analýzy zvoleného algoritmu. Po jeho stisknutí aplikace vytvoří *10 separátních testů*. V každém testu je vygenerováno *náhodné pole*. Při prvním testu je velikost pole `50`, v každém následujícím je velikost pole zvýšena o `50`. Během řazení dochází k automatickému měření:

- *počtu elementárních operací* (například podmínky uvnitř cyklů, volání funkcí, aritmetické operace)
- *využití paměti na zásobníku a haldě* (jejich maximální využití v konkrétní časový okamžik)

Následně jsou hodnoty normalizovány a jsou porovnány s podporovanými asymptotickými modely:

- `O(1)`
- `O(log (n))`
- `O(n)`
- `O(n log (n))`
- `O(n^2)`
- `O(n^3)`

K porovnání se používá *metoda nejmenších čtverců* s využitím koeficientu determinace `R^2`.

### Vizualizace řazení
K vizualizaci slouží tlačítko `Visualize`. K tomuto tlačítku se vztahuje i `posuvník` po pravé části. `Posuvník` určuje velikost pole (mezi `10` - `100`), které má být řazeno. Po stisknutí tlačítka se inicializuje náhodné pole a dojde k řazení. Během toho dochází k detekci pomocí maker:
- `SWAP` - výměna dvou prvků, zaznamenána *červeně*,
- `TRACK_CHANGE` - výměna hodnoty prvku na konkrétní pozici, vizualizována *modře*.
Nedotčené položky jsou zaznamenány *šedou* barvou.

Změny se uloží a po kompletním seřazení dochází k přehrání animace s využitím `matplotlib`.

## Vlastní algoritmy a použití maker
Pro korektní chování aplikace je potřeba používat předdefinovaná makra, které zapouzdřují výpočet naměřených *elementárních operací* a maximální využití *zásobníku* a *haldy*:

- `FOR` - makro nahrazující cyklus `for` 
  - *syntax*: `FOR(výraz1, výraz2, výraz3)`
  - *příklad*: `FOR(int i = 5, i < 10, ++i) {printf("Hello World!");}` - **využívá jako oddělovač čárku namísto středníku**.

- `WHILE` - makro nahrazující cyklus `while` 
  - *syntax*: `WHILE(podmínka)`
  - *příklad*: `WHILE(1) {printf("Nejak jsem se zacyklil!");}`

- `IF` - makro nahrazující podmínku `if` 
  - *syntax*: `IF(podmínka)`
  - *příklad*: `IF(vek < 18) {printf("Promin, ale nemuzes volit.");}`

- `CALL_FUNCTION_VOID` - makro k volání funkce bez návratové hodnoty
  - *syntax*: `CALL_FUNCTION_VOID(func, ...);`, kde `...` jsou parametry funkce `func`.
  - *příklad*: `CALL_FUNCTION_VOID(bez_navratu, parametr1, parametr2);`, kde funkce `bez_navratu` přebírá argumenty `parametr1` a `parametr2`.

- `CALL_FUNCTION_RETURN` - makro k volání funkce s návratovou hodnotou
  - *syntax*: `CALL_FUNCTION_RETURN(func, ...);`, kde `...` jsou parametry funkce `func`.
  - *příklad*: `int i = CALL_FUNCTION_RETURN(s_navratem, parametr1, parametr2);`, kde funkce `s_navratem` přebírá argumenty `parametr1` a `parametr2`.

- `SWAP` - makro pro detekci prohození dvou prvků uvnitř hlavního pole
  - *syntax*: `SWAP(a, b, pomocna)`, kde `a` a `b` jsou prvky pole a `pomocna` je dočasná proměnná pro prohození prvků.
  - *příklad*: `SWAP(arr[i], arr[j], pomocna)` 

- `TRACK_CHANGE` - makro pro detekci změny na konkrétní pozici *hlavního pole*. (například změna prvků hlavního pole a pomocného pole pro `merge sort`)
  - *syntax*: `TRACK_CHANGE(index_zmeny)`, kde `index` je pozice zaznamenané změny.
  - *příklad*: `TRACK_CHANGE(i)`

- `ADD` - makro pro součet dvou prvků
  - *syntax*: `ADD(citatel1, citatel2)`
  - *příklad*: `int soucet = ADD(a, b)`

- `SUBTRACT` - makro pro rozdíl dvou prvků
  - *syntax*: `SUBTRACT(mensenec, mensitel)`
  - *příklad*: `int rozdil = SUBTRACT(a, b)`

- `MULTIPLY` - makro pro násobení dvou prvků
  - *syntax*: `MULTIPLY(cinitel1, cinitel2)`
  - *příklad*: `int soucin = MULTIPLY(a, b)`

- `DIVIDE` - makro pro dělení dvou prvků
  - *syntax*: `DIVIDE(delenec, delitel)`
  - *příklad*: `double podil = DIVIDE(a, b)`