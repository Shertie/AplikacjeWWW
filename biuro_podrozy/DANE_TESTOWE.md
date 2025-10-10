# Przykładowe dane testowe dla Biura Podróży

## Po utworzeniu superusera, możesz dodać następujące dane testowe przez panel administracyjny

### 1. Kraje (<http://127.0.0.1:8000/admin/wycieczki/kraj/>)

|Kraj|Skrót|Kontynent|
|---|---|---|
|Polska | PL | Europa|
|Hiszpania | ES | Europa|
|Włochy | IT | Europa|
|Grecja | GR | Europa|
|Egipt | EG | Afryka|
|Tajlandia | TH | Azja|

### 2. Linie Lotnicze (<http://127.0.0.1:8000/admin/wycieczki/linialotnicza/>)

|Linia lotnicza|Skrót|Kraj|Strona internetowa|
|--|--|--|--|
LOT Polish Airlines | LOT | Polska | <www.lot.com>
Lufthansa | LH | Niemcy | <www.lufthansa.com>
Ryanair | FR | Irlandia | <www.ryanair.com>
Wizz Air | W6 | Węgry | <www.wizzair.com>

### 3. Loty (<http://127.0.0.1:8000/admin/wycieczki/lot/>)

|Nr lotu| Linia lotnicza| Lotnisko początkowe| Lotnisko końcowe|Data startu|Data lądowania|Czas lotu|
|--|--|--|--|--|--|--|
LOT123 | LOT | Warszawa Okęcie | Barcelona El Prat | 2025-12-15 08:00 | 2025-12-15 11:30 | 3:30
FR456 | Ryanair | Kraków Balice | Rzym Fiumicino | 2025-12-20 10:00 | 2025-12-20 13:00 | 3:00
LH789 | Lufthansa | Warszawa | Ateny | 2026-01-10 14:00 | 2026-01-10 18:00 | 4:00

### 4. Hotele (<http://127.0.0.1:8000/admin/wycieczki/hotel/>)

|Hotel|Kraj|Miasto|Adres|Opinie|
|--|--|--|--|--|
Grand Hotel Barcelona | Hiszpania | Barcelona | ul. Rambla 123 | 5⭐
Hotel Roma Centro | Włochy | Rzym | Via Roma 45 | 4⭐
Acropolis View Hotel | Grecja | Ateny | Plaka District 12 | 4⭐
Seaside Resort | Grecja | Kreta | Beach Road 1 | 5⭐

Opis hoteli:

- Grand Hotel Barcelona: "Luksusowy hotel w centrum Barcelony z widokiem na Sagradę Familię"
- Hotel Roma Centro: "Komfortowy hotel blisko Koloseum i Forum Romanum"
- Acropolis View Hotel: "Hotel z zapierającym dech w piersiach widokiem na Akropol"

Udogodnienia: "Basen, SPA, siłownia, restauracja, bar, Wi-Fi, klimatyzacja"

### 5. Wycieczki (<http://127.0.0.1:8000/admin/wycieczki/wycieczka/>)

#### Wycieczka 1: "Magiczna Barcelona - 7 dni"

- Kraj: Hiszpania
- Hotel: Grand Hotel Barcelona
- Lot tam: LOT123
- Data: 2025-12-15 do 2025-12-22
- Dni/Noce: 7/6
- Opcja: PREMIUM
- Cena za osobę: 3500 PLN
- Cena dziecko: 2500 PLN
- Max osób: 30
- Aktywna: ✓

Opis: "Poznaj urokliwą Barcelonę! Zwiedzanie Sagrady Familii, Park Güell, La Rambla, Gothic Quarter. Wieczory na plaży przy Barcelonecie."

#### Wycieczka 2: "Rzym - Wieczne Miasto"

- Kraj: Włochy
- Hotel: Hotel Roma Centro
- Lot tam: FR456
- Data: 2025-12-20 do 2025-12-27
- Dni/Noce: 7/6
- Opcja: STANDARD
- Cena za osobę: 2800 PLN
- Cena dziecko: 2000 PLN
- Max osób: 25
- Aktywna: ✓

Opis: "Odkryj starożytny Rzym! Koloseum, Forum Romanum, Fontanna di Trevi, Watykan z Kaplicą Sykstyńską."

#### Wycieczka 3: "Greckie Wakacje - Ateny i Kreta"

- Kraj: Grecja
- Hotel: Acropolis View Hotel
- Lot tam: LH789
- Data: 2026-01-10 do 2026-01-17
- Dni/Noce: 7/6
- Opcja: LUXURY
- Cena za osobę: 4200 PLN
- Cena dziecko: 3000 PLN
- Max osób: 20
- Aktywna: ✓

Opis: "Wycieczka łącząca historię Aten z relaksem na Krecie. Akropol, Partenon, pla że z czystym morzem."

### 6. Klienci (<http://127.0.0.1:8000/admin/wycieczki/klient/>)

|Imię|Nazwisko|E-mail|Nr tel.|Adres zamieszkania|Kraj|
|--|--|--|--|--|--|
Jan | Kowalski | jan.kowalski@email.pl | +48 123 456 789 | ul. Warszawska 1, 00-001 Warszawa | Polska
Anna | Nowak | anna.nowak@email.pl | +48 234 567 890 | ul. Krakowska 23, 30-001 Kraków | Polska
Piotr | Wiśniewski | piotr.wisniewski@email.pl | +48 345 678 901 | ul. Gdańska 45, 80-001 Gdańsk | Polska


### 7. Rezerwacje (<http://127.0.0.1:8000/admin/wycieczki/rezerwacja/>)

#### Rezerwacja 1

- Klient: Jan Kowalski
- Wycieczka: Magiczna Barcelona
- Status: OPLACONA
- Dorośli: 2, Dzieci: 1
- Cena całkowita: 9500 PLN
- Zaliczka: 9500 PLN
- Data rezerwacji: 2025-11-01

#### Rezerwacja 2

- Klient: Anna Nowak
- Wycieczka: Rzym - Wieczne Miasto
- Status: POTWIERDZONA
- Dorośli: 2, Dzieci: 0
- Cena całkowita: 5600 PLN
- Zaliczka: 1680 PLN (30%)
- Data rezerwacji: 2025-11-15

#### Rezerwacja 3

- Klient: Piotr Wiśniewski
- Wycieczka: Greckie Wakacje
- Status: OCZEKUJACA
- Dorośli: 2, Dzieci: 2
- Cena całkowita: 14400 PLN
- Zaliczka: 0 PLN
- Data rezerwacji: 2025-11-20

### 8. Opinie (<http://127.0.0.1:8000/admin/wycieczki/opinia/>)

#### Opinia 1

- Wycieczka: Magiczna Barcelona
- Klient: Jan Kowalski
- Rezerwacja: #1
- Ocena: 5⭐
- Tytuł: "Wspaniałe przeżycie!"
- Treść: "Barcelona to cudowne miasto! Hotel był świetny, Sagrada Familia zachwyciła nas wszystkich. Organizacja na najwyższym poziomie. Polecam!"
- Ocena hotelu: 5
- Ocena lotu: 4
- Ocena obsługi: 5
- Zweryfikowana: ✓

#### Opinia 2

- Wycieczka: Rzym - Wieczne Miasto
- Klient: Anna Nowak
- Ocena: 4⭐
- Tytuł: "Bardzo dobra wycieczka"
- Treść: "Rzym jest przepiękny! Zwiedziliśmy wszystkie najważniejsze zabytki. Hotel blisko centrum, co było bardzo wygodne. Jedyny minus - tłumy turystów."
- Ocena hotelu: 4
- Ocena lotu: 3
- Ocena obsługi: 5
- Zweryfikowana: ✓

---

## Kolejność dodawania danych

1. Kraje (są wymagane dla innych modeli)
2. Linie Lotnicze
3. Loty
4. Hotele
5. Wycieczki
6. Klienci
7. Rezerwacje
8. Opinie

## Testowanie CRUD

Po dodaniu danych testowych, przetestuj:

### CREATE (Tworzenie)

- Dodaj nową wycieczkę przez panel admin
- Dodaj nowego klienta
- Utwórz nową rezerwację

### READ (Odczyt)

- Przeglądaj listy wszystkich modeli
- Użyj filtrów (np. wycieczki aktywne, rezerwacje opłacone)
- Wyszukaj wycieczki po nazwie kraju

### UPDATE (Aktualizacja)

- Zmień status rezerwacji z OCZEKUJĄCA na POTWIERDZONA
- Zaktualizuj cenę wycieczki
- Zmodyfikuj dane klienta

### DELETE (Usuwanie)

- Usuń testową opinię
- Usuń nieaktywną wycieczkę
- Uwaga: Kaskadowe usuwanie zabezpiecza integralność danych

## Obserwacje

- Średnia ocena wycieczki automatycznie się aktualizuje po dodaniu opinii
- Pozostała kwota w rezerwacji oblicza się automatycznie
- Status rezerwacji jest kolorowy w panelu admin
- Gwiazdki ⭐ wyświetlają się w ocenach
- Panel admin ma zaawansowane filtry i wyszukiwanie
