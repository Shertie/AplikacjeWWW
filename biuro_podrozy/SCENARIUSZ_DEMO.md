# 🎬 Scenariusz Prezentacji Aplikacji Biura Podróży (EchoAPI for VS Code)

Ten dokument zawiera kompletny scenariusz prezentacji systemu "od A do Z", przygotowany specjalnie pod kątem rozszerzenia **EchoAPI for VS Code**.

## 🛠️ 1. Przygotowanie Środowiska (EchoAPI)

Zanim zaczniesz prezentację, skonfiguruj środowisko w EchoAPI, aby nie wpisywać ręcznie adresów i tokenów.

1. Otwórz panel **EchoAPI** w VS Code (ikona w pasku bocznym).
2. W sekcji **Environments** (prawy górny róg panelu EchoAPI) utwórz nowe środowisko o nazwie `Biuro Podróży Local`.
3. Dodaj zmienną:
    * **Variable:** `baseUrl`
    * **Local Value:** `http://127.0.0.1:8000` (Cloud Value można pominąć)
4. Dodaj zmienną (pustą na start):
    * **Variable:** `token`
    * **Local Value:** `(zostaw puste)`
5. Zapisz środowisko i wybierz je jako aktywne.

---

## 🔐 2. Autentykacja (Pobranie Tokenu)

Zaczynamy od zalogowania się jako administrator, aby uzyskać token niezbędny do edycji danych.

1. Utwórz nowy request w EchoAPI:
    * **Nazwa:** `1. Login (Get Token)`
    * **Metoda:** `POST`
    * **URL:** `{{baseUrl}}/api-token-auth/`
2. W zakładce **Body** wybierz `JSON` i wklej:

    ```json
    {
        "username": "admin",
        "password": "password123"
    }
    ```

    *(Upewnij się, że taki użytkownik istnieje w bazie - `python manage.py createsuperuser`)*
3. W zakładce **Tests** (lub Post-response script) dodaj skrypt, który automatycznie zapisze token do zmiennej środowiskowej:

    ```javascript
    var jsonData = JSON.parse(responseBody);
    pm.environment.set("token", jsonData.token);
    ```

4. **Wyślij (Send)**.
    * ✅ **Oczekiwany wynik:** Status `200 OK` i JSON z tokenem.
    * 👀 **Sprawdź:** Zmienna środowiskowa `token` powinna być teraz wypełniona.

---

## 🌍 3. Zarządzanie Krajami (CRUD)

Pokażemy, że baza jest pusta, a następnie dodamy pierwszy kraj.

### A. Pobranie listy krajów (Pusta lista)

1. Nowy request: `2. Get Kraje`
2. **Metoda:** `GET`
3. **URL:** `{{baseUrl}}/api/kraje/`
4. **Wyślij**.
    * ✅ **Wynik:** `200 OK`, pusta lista `[]` (lub lista istniejących krajów).

### B. Dodanie Kraju (Włochy)

1. Nowy request: `3. Create Kraj (Włochy)`
2. **Metoda:** `POST`
3. **URL:** `{{baseUrl}}/api/kraje/`
4. **Auth:** Wybierz Type `API Key` -> Key: `Authorization`, Value: `Token {{token}}`, Add to: `Header`. (Lub ręcznie w Headers: `Authorization`: `Token {{token}}`).
5. **Body (JSON):**

    ```json
    {
        "nazwa": "Włochy",
        "kod": "IT",
        "kontynent": "Europa",
        "opis": "Kraj pizzy, makaronu i historii."
    }
    ```

6. **Wyślij**.
    * ✅ **Wynik:** `201 Created`. Zwrócony obiekt z `id: 1`.

---

## ✈️ 4. Linie Lotnicze i Loty (Walidacja)

Teraz dodamy linię lotniczą i spróbujemy dodać lot z błędem logicznym (data przylotu przed wylotem).

### A. Dodanie Linii Lotniczej

1. Nowy request: `4. Create Linia (Ryanair)`
2. **Metoda:** `POST`
3. **URL:** `{{baseUrl}}/api/linie-lotnicze/`
4. **Headers:** `Authorization`: `Token {{token}}`
5. **Body (JSON):**

    ```json
    {
        "nazwa": "Ryanair",
        "kod_iata": "FR",
        "kraj_pochodzenia": 1
    }
    ```

6. **Wyślij**.
    * ✅ **Wynik:** `201 Created`.

### B. Próba dodania błędnego lotu (Walidacja)

1. Nowy request: `5. Create Lot (Error)`
2. **Metoda:** `POST`
3. **URL:** `{{baseUrl}}/api/loty/`
4. **Headers:** `Authorization`: `Token {{token}}`
5. **Body (JSON):**

    ```json
    {
        "numer_lotu": "FR1234",
        "linia_lotnicza": 1,
        "lotnisko_wylotu": "Warszawa (WAW)",
        "lotnisko_przylotu": "Rzym (CIA)",
        "data_wylotu": "2024-07-10T10:00:00Z",
        "data_przylotu": "2024-07-10T08:00:00Z", 
        "czas_trwania": "02:00:00"
    }
    ```

6. **Wyślij**.
    * ❌ **Wynik:** `400 Bad Request`.
    * **Komunikat:** `["Data przylotu musi być późniejsza niż data wylotu."]`

### C. Poprawa danych lotu

1. Zmień w Body `data_przylotu` na `"2024-07-10T12:00:00Z"`.
2. **Wyślij ponownie**.
    * ✅ **Wynik:** `201 Created`. (Zapisz ID tego lotu, np. `1`).

### D. Dodanie lotu powrotnego

1. Zmień Body na lot powrotny (Rzym -> Warszawa) z późniejszą datą (np. 17 lipca).
2. **Wyślij**.
    * ✅ **Wynik:** `201 Created`. (ID: `2`).

---

## 🏨 5. Hotele i Wycieczki (Logika Biznesowa)

Pokażemy walidację spójności danych: Hotel musi być w tym samym kraju co wycieczka.

### A. Dodanie Hotelu (Włochy)

1. Nowy request: `6. Create Hotel (Rzym)`
2. **Metoda:** `POST`
3. **URL:** `{{baseUrl}}/api/hotele/`
4. **Headers:** `Authorization`: `Token {{token}}`
5. **Body (JSON):**

    ```json
    {
        "nazwa": "Hotel Colosseum",
        "kraj": 1, 
        "miasto": "Rzym",
        "adres": "Via Roma 1",
        "kategoria": 4,
        "opis": "Widok na Koloseum.",
        "udogodnienia": "WiFi, Śniadanie"
    }
    ```

6. **Wyślij**.
    * ✅ **Wynik:** `201 Created`.

### B. Próba dodania wycieczki z błędem (Niezgodność kraju)

Załóżmy, że próbujemy zrobić wycieczkę do **Hiszpanii** (której jeszcze nie ma, lub ma inne ID), ale używamy hotelu we **Włoszech**.

1. Najpierw dodajmy Hiszpanię (opcjonalnie, aby ID=2 istniało):
    * Szybki POST na `/api/kraje/` z `{"nazwa": "Hiszpania", "kod": "ES", "kontynent": "Europa"}`. -> ID: `2`.
2. Nowy request: `7. Create Wycieczka (Error)`
3. **Metoda:** `POST`
4. **URL:** `{{baseUrl}}/api/wycieczki/`
5. **Headers:** `Authorization`: `Token {{token}}`
6. **Body (JSON):**

    ```json
    {
        "nazwa": "Błąd Logiczny",
        "opis": "Test walidacji",
        "kraj_docelowy": 2, 
        "hotel": 1,
        "lot_tam": 1,
        "lot_powrot": 2
    }
    ```

    *(Kraj docelowy ID=2 (Hiszpania), a Hotel ID=1 (Włochy))*
7. **Wyślij**.
    * ❌ **Wynik:** `400 Bad Request`.
    * **Komunikat:** `["Hotel musi znajdować się w kraju docelowym wycieczki."]`

### C. Utworzenie poprawnej wycieczki

1. Zmień `kraj_docelowy` na `1` (Włochy).
2. **Wyślij ponownie**.
    * ✅ **Wynik:** `201 Created`.

---

## 🚀 6. GraphQL - Agregacja Danych

Na koniec pokażemy "killer feature" GraphQL - pobranie wszystkich danych jednym zapytaniem, zamiast odpytywać 5 endpointów REST.

1. Nowy request: `8. GraphQL Full Data`
2. **Metoda:** `POST`
3. **URL:** `{{baseUrl}}/graphql/`
4. **Body:** Wybierz typ `GraphQL`.
5. **Query:**

    ```graphql
    query {
      allWycieczki {
        id
        nazwa
        opis
        krajDocelowy {
          nazwa
          kontynent
        }
        hotel {
          nazwa
          kategoria
          miasto
        }
        lotTam {
          numerLotu
          dataWylotu
          liniaLotnicza {
            nazwa
          }
        }
      }
    }
    ```

6. **Wyślij**.
    * ✅ **Wynik:** JSON zawierający pełne drzewo danych: Wycieczka -> Kraj, Hotel, Lot -> Linia Lotnicza.

---

## 🧹 7. Sprzątanie (Opcjonalnie)

Aby zostawić bazę czystą po demo.

1. Request `DELETE` na `{{baseUrl}}/api/wycieczki/1/`
2. Request `DELETE` na `{{baseUrl}}/api/hotele/1/`
3. Itd.
