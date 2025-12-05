# 📘 Instrukcja korzystania z aplikacji (EchoAPI)

Poniżej znajduje się krótka instrukcja uruchomienia i testowania API Biura Podróży przy użyciu narzędzia EchoAPI (lub Postman/Insomnia).

## 1. Uruchomienie projektu

Przed rozpoczęciem testowania upewnij się, że serwer działa.

1. **Przejdź do katalogu projektu:**

    ```bash
    cd biuro_podrozy
    ```

2. **Przygotuj bazę danych (jeśli to pierwsze uruchomienie):**

    ```bash
    python3 manage.py migrate
    ```

3. **Utwórz użytkownika administracyjnego (do testowania autentykacji):**

    ```bash
    python3 manage.py createsuperuser
    ```

    *(Postępuj zgodnie z instrukcjami w terminalu, podając nazwę użytkownika i hasło)*

4. **Uruchom serwer:**

    ```bash
    python3 manage.py runserver
    ```

    Serwer będzie dostępny pod adresem: `http://127.0.0.1:8000/`

---

## 2. Konfiguracja EchoAPI

### A. Autentykacja (Uzyskanie Tokenu)

Większość operacji modyfikujących dane (POST, PUT, DELETE) wymaga zalogowania.

1. Utwórz nowe żądanie **POST**.
2. URL: `http://127.0.0.1:8000/api-token-auth/`
3. **Body** (JSON):

    ```json
    {
        "username": "twoj_login",
        "password": "twoje_haslo"
    }
    ```

4. Wyślij żądanie. W odpowiedzi otrzymasz token:

    ```json
    {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    }
    ```

### B. Używanie Tokenu

W kolejnych zapytaniach dodaj nagłówek autoryzacyjny:

* **Key:** `Authorization`
* **Value:** `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b` (zastąp tokenem z poprzedniego kroku)

---

## 3. Przykładowe testy REST API

### 🌍 Kraje

* **Lista krajów (GET):** `http://127.0.0.1:8000/api/kraje/`
* **Szczegóły kraju (GET):** `http://127.0.0.1:8000/api/kraje/1/`
* **Dodanie kraju (POST):**
  * URL: `http://127.0.0.1:8000/api/kraje/`
  * Body (JSON):

```json
{
    "nazwa": "Hiszpania",
    "kod": "ES",
    "kontynent": "Europa",
    "opis": "Słoneczny kraj na Półwyspie Iberyjskim."
}
```

### 🎒 Wycieczki

* **Lista wycieczek (GET):** `http://127.0.0.1:8000/api/wycieczki/`
* **Dodanie wycieczki (POST):**
  * URL: `http://127.0.0.1:8000/api/wycieczki/`
  * Body (JSON):

```json
{
    "nazwa": "Wakacje w Barcelonie",
    "opis": "Tydzień zwiedzania i plażowania.",
    "kraj_docelowy": 1,
    "hotel": 1,
    "lot_tam": 1,
    "lot_powrot": 2
}
```

>(Upewnij się, że ID kraju, hotelu i lotów istnieją)*

---

## 4. Testowanie GraphQL

* **Endpoint:** `http://127.0.0.1:8000/graphql/`
* **Metoda:** POST

### Przykładowe Query (Pobieranie danych)

W sekcji Body wybierz **GraphQL** i wklej:

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
    }
  }
}
```

### Przykładowa Mutation (Dodawanie danych)

```graphql
mutation {
  createKraj(nazwa: "Włochy", kod: "IT", kontynent: "Europa", opis: "Kraj pizzy i makaronu") {
    kraj {
      id
      nazwa
    }
  }
}
```
