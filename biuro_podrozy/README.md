# 🌴 Biuro Podróży - System Zarządzania Wycieczkami

Backend Django dla systemu zarządzania biurem podróży z pełnym CRUD i panelem administracyjnym.

## 📋 Spis treści

- [Opis projektu](#opis-projektu)
- [Modele danych](#modele-danych)
- [Relacje](#relacje)
- [Funkcjonalności](#funkcjonalności)
- [Instalacja](#instalacja)
- [Panel administracyjny](#panel-administracyjny)
- [API REST](#api-rest-opcjonalne)

## 🎯 Opis projektu

System backendowy dla biura podróży umożliwiający kompleksowe zarządzanie:

- Wycieczkami i ofertami
- Rezerwacjami klientów
- Lotami i liniami lotniczymi
- Hotelami w różnych krajach
- Opiniami i ocenami (system 1-5 gwiazdek)
- Cenami i opcjami cenowymi (Standard/Premium/Luxury)
- Statusami rezerwacji (Oczekująca/Potwierdzona/Opłacona/Anulowana/Zakończona)

## 📊 Modele danych

### 1. **Kraj** 🌍

Reprezentuje kraje docelowe wycieczek.

**Pola:**

- `nazwa` - Nazwa kraju (unique)
- `kod` - Kod ISO kraju (np. PL, FR) (unique)
- `kontynent` - Nazwa kontynentu
- `opis` - Opis kraju

**Relacje:**

- One-to-Many → Hotel
- One-to-Many → Wycieczka
- One-to-Many → Klient
- One-to-Many → LiniaLotnicza

### 2. **LiniaLotnicza** ✈️

Linie lotnicze obsługujące loty.

**Pola:**

- `nazwa` - Nazwa linii lotniczej
- `kod_iata` - Kod IATA (np. LOT, LH) (unique)
- `kraj_pochodzenia` - ForeignKey → Kraj
- `strona_www` - URL strony internetowej

**Relacje:**

- One-to-Many → Lot

### 3. **Lot** 🛫

Szczegóły lotów dla wycieczek.

**Pola:**

- `numer_lotu` - Numer lotu (unique)
- `linia_lotnicza` - ForeignKey → LiniaLotnicza
- `lotnisko_wylotu` - Nazwa lotniska wylotu
- `lotnisko_przylotu` - Nazwa lotniska przylotu
- `data_wylotu` - Data i czas wylotu
- `data_przylotu` - Data i czas przylotu
- `czas_trwania` - Czas trwania lotu (DurationField)

**Relacje:**

- One-to-Many → Wycieczka (jako lot_tam)
- One-to-Many → Wycieczka (jako lot_powrot)

### 4. **Hotel** 🏨

Hotele dostępne w ofercie.

**Pola:**

- `nazwa` - Nazwa hotelu
- `kraj` - ForeignKey → Kraj
- `miasto` - Miasto
- `adres` - Adres
- `kategoria` - Kategoria gwiazdkowa (1-5) ⭐
- `opis` - Opis hotelu
- `udogodnienia` - Lista udogodnień
- `strona_www` - URL strony hotelu

**Relacje:**

- One-to-Many → Wycieczka

### 5. **Wycieczka** 🎒

Główny model - oferowane wycieczki.

**Pola:**

- `nazwa` - Nazwa wycieczki
- `opis` - Szczegółowy opis (TextField)
- `kraj_docelowy` - ForeignKey → Kraj
- `hotel` - ForeignKey → Hotel
- `lot_tam` - ForeignKey → Lot
- `lot_powrot` - ForeignKey → Lot (optional)
- `data_rozpoczecia` - Data rozpoczęcia
- `data_zakonczenia` - Data zakończenia
- `liczba_dni` - Liczba dni
- `liczba_nocy` - Liczba nocy
- `opcja_cenowa` - Wybór: STANDARD/PREMIUM/LUXURY
- `cena_za_osobe` - Cena za osobę dorosłą
- `cena_dziecko` - Cena za dziecko (optional)
- `max_liczba_osob` - Maksymalna liczba uczestników
- `aktywna` - Czy wycieczka jest dostępna
- `created_at` - Data utworzenia
- `updated_at` - Data aktualizacji

**Metody:**

- `srednia_ocena` - Property obliczający średnią ocenę z opinii

**Relacje:**

- One-to-Many → Rezerwacja
- One-to-Many → Opinia

### 6. **Klient** 👤

Klienci biura podróży.

**Pola:**

- `user` - OneToOneField → User (optional, dla zalogowanych)
- `imie` - Imię
- `nazwisko` - Nazwisko
- `email` - Email (unique)
- `telefon` - Numer telefonu
- `adres` - Adres
- `kod_pocztowy` - Kod pocztowy
- `miasto` - Miasto
- `kraj` - ForeignKey → Kraj (optional)
- `data_rejestracji` - Data rejestracji

**Relacje:**

- One-to-Many → Rezerwacja
- One-to-Many → Opinia

### 7. **Rezerwacja** 📝

Rezerwacje wycieczek przez klientów.

**Pola:**

- `klient` - ForeignKey → Klient
- `wycieczka` - ForeignKey → Wycieczka
- `status` - Status rezerwacji (OCZEKUJACA/POTWIERDZONA/OPLACONA/ANULOWANA/ZAKONCZONA)
- `liczba_doroslich` - Liczba osób dorosłych
- `liczba_dzieci` - Liczba dzieci
- `cena_calkowita` - Całkowita cena
- `zaliczka` - Wpłacona zaliczka
- `pozostalo_do_zaplaty` - Pozostała kwota (obliczane automatycznie)
- `data_rezerwacji` - Data złożenia rezerwacji
- `data_potwierdzenia` - Data potwierdzenia (optional)
- `data_oplaty` - Data pełnej opłaty (optional)
- `uwagi` - Dodatkowe uwagi

**Metody:**

- `save()` - Nadpisana metoda automatycznie obliczająca pozostałą kwotę

**Relacje:**

- One-to-One → Opinia

### 8. **Opinia** ⭐

Opinie i oceny wycieczek.

**Pola:**

- `wycieczka` - ForeignKey → Wycieczka
- `klient` - ForeignKey → Klient
- `rezerwacja` - OneToOneField → Rezerwacja (optional)
- `ocena` - Ocena główna (1-5)
- `tytul` - Tytuł opinii
- `tresc` - Treść opinii (TextField)
- `ocena_hotelu` - Ocena hotelu (1-5, optional)
- `ocena_lotu` - Ocena lotu (1-5, optional)
- `ocena_obslugi` - Ocena obsługi (1-5, optional)
- `data_dodania` - Data dodania opinii
- `zweryfikowana` - Czy opinia jest zweryfikowana

**Ograniczenia:**

- `unique_together` - Jeden klient może dodać tylko jedną opinię do danej wycieczki

## 🔗 Relacje między modelami

```
Kraj (1) ←→ (M) LiniaLotnicza
Kraj (1) ←→ (M) Hotel
Kraj (1) ←→ (M) Wycieczka
Kraj (1) ←→ (M) Klient

LiniaLotnicza (1) ←→ (M) Lot

Lot (1) ←→ (M) Wycieczka (jako lot_tam)
Lot (1) ←→ (M) Wycieczka (jako lot_powrot)

Hotel (1) ←→ (M) Wycieczka

Wycieczka (1) ←→ (M) Rezerwacja
Wycieczka (1) ←→ (M) Opinia

Klient (1) ←→ (M) Rezerwacja
Klient (1) ←→ (M) Opinia

Rezerwacja (1) ←→ (1) Opinia
```

## ✨ Funkcjonalności

### Panel Administracyjny (CRUD)

Każdy model ma zaawansowaną konfigurację panelu admin z:

- **Wyświetlaniem list** z kluczowymi informacjami
- **Filtrami** według różnych kryteriów
- **Wyszukiwaniem** pełnotekstowym
- **Sortowaniem** i hierarchią dat
- **Kolorowaniem** statusów i stanów
- **Inlines** dla powiązanych obiektów
- **Obliczeniami** (średnia ocena, liczba rezerwacji, etc.)
- **Custom actions** i metodami

#### Szczególne funkcje

**Wycieczka:**

- Inline rezerwacji i opinii
- Automatyczna średnia ocena
- Status aktywności (aktywna/nieaktywna)
- Pełne info o okresie i cenach

**Rezerwacja:**

- Kolorowy status rezerwacji
- Automatyczne obliczanie pozostałej kwoty
- Podświetlanie nieopłaconych rezerwacji
- Szczegółowe informacje o uczestnikach

**Opinia:**

- System gwiazdek ⭐
- Szczegółowe oceny (hotel/lot/obsługa)
- Status weryfikacji
- Ograniczenie: 1 opinia/klient/wycieczka

**Hotel:**

- Kategoria gwiazdkowa
- Liczba dostępnych wycieczek
- Pełne informacje kontaktowe

## 🚀 Instalacja

### 1. Klonowanie repozytorium

```bash
git clone <url-repozytorium>
cd AplikacjeWWW/biuro_podrozy
```

### 2. Środowisko wirtualne

```bash
# Z katalogu głównego projektu
cd ..
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

### 3. Instalacja zależności

```bash
pip install django
```

### 4. Migracje bazy danych

```bash
cd biuro_podrozy
python manage.py migrate
```

### 5. Utworzenie superusera

```bash
python manage.py createsuperuser
```

### 6. Uruchomienie serwera

```bash
python manage.py runserver
```

### 7. Dostęp do panelu administracyjnego

Otwórz przeglądarkę: **<http://127.0.0.1:8000/admin/>**

## 🎨 Panel Administracyjny

### Funkcje CRUD dla każdego modelu

#### **Create (Tworzenie)**

- Dodawanie nowych rekordów przez formularz
- Walidacja danych po stronie backendu
- Automatyczne generowanie timestamps

#### **Read (Odczyt)**

- Listy z filtrowaniem
- Wyszukiwanie pełnotekstowe
- Sortowanie wielokolumnowe
- Szczegółowy widok pojedynczego rekordu

#### **Update (Aktualizacja)**

- Edycja istniejących rekordów
- Inline editing dla powiązanych obiektów
- Historia zmian (Django admin history)

#### **Delete (Usuwanie)**

- Usuwanie pojedynczych rekordów
- Masowe usuwanie (bulk delete)
- Ochrona przed kaskadowym usunięciem (gdzie skonfigurowane)

### Przykładowe dane testowe

Po uruchomieniu możesz dodać przykładowe dane:

1. **Kraje**: Polska, Hiszpania, Włochy, Grecja
2. **Linie lotnicze**: LOT, Lufthansa, Ryanair
3. **Loty**: Różne połączenia międzynarodowe
4. **Hotele**: Hotele 3-5 gwiazdkowe w różnych krajach
5. **Wycieczki**: Kombinacje hoteli i lotów z cenami
6. **Klienci**: Testowi klienci
7. **Rezerwacje**: Przykładowe rezerwacje z różnymi statusami
8. **Opinie**: Oceny wycieczek z różnymi ratingami

## 🔌 API REST (Opcjonalne)

### Instalacja Django REST Framework

```bash
pip install djangorestframework
```

### Dodanie do INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'wycieczki',
]
```

### Utworzenie serializers i viewsets

Możliwe rozszerzenie o pełne REST API z endpointami:

- `/api/wycieczki/` - Lista i szczegóły wycieczek
- `/api/rezerwacje/` - Zarządzanie rezerwacjami
- `/api/opinie/` - Dodawanie i przeglądanie opinii
- `/api/hotele/` - Lista hoteli
- etc.

## 📁 Struktura projektu

```
biuro_podrozy/
├── manage.py
├── db.sqlite3
├── biuro_podrozy/          # Konfiguracja projektu
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── wycieczki/              # Aplikacja główna
    ├── __init__.py
    ├── admin.py            # Konfiguracja panelu admin
    ├── apps.py
    ├── models.py           # 8 modeli danych
    ├── tests.py
    ├── views.py
    └── migrations/
        └── 0001_initial.py # Migracja z wszystkimi modelami
```

## 🎯 Kluczowe cechy implementacji

✅ **Pełny CRUD** dla wszystkich modeli  
✅ **System ocen 1-5 gwiazdek** ⭐  
✅ **Opcje cenowe** (Standard/Premium/Luxury)  
✅ **Statusy rezerwacji** (5 statusów z kolorowaniem)  
✅ **Automatyczne obliczenia** (pozostała kwota, średnia ocena)  
✅ **Walidacja danych** (validators dla ocen, cen, dat)  
✅ **Relacje Foreign Key** zgodnie z wymaganiami  
✅ **Zaawansowany panel admin** z inline editing  
✅ **Timestamps** (created_at, updated_at)  
✅ **Unique constraints** (email klienta, opinie)  
✅ **Custom metody** i properties w modelach  
✅ **Dokumentacja inline** (docstrings, help_text)  

## 👨‍💻 Autor

Projekt stworzony jako backend Django dla systemu zarządzania biurem podróży.

## 📝 Licencja

Projekt edukacyjny.
