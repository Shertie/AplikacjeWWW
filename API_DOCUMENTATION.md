# Dokumentacja API - Przykłady użycia

## Wprowadzenie

Poniżej znajdują się przykłady użycia API dla aplikacji blogowej. Wszystkie endpointy są dostępne pod prefiksem `/api/`.

API obsługuje operacje CRUD (Create, Read, Update, Delete) dla trzech głównych encji:
- **Category** (Kategoria)
- **Topic** (Temat)
- **Post** (Post)

## Przygotowanie środowiska

Przed rozpoczęciem testów upewnij się, że:
1. Serwer Django działa: `python manage.py runserver`
2. Masz zainstalowany `curl` lub `Postman`
3. Utworzyłeś użytkownika i posiadasz odpowiednie uprawnienia

## Struktura endpointów

### Category (Kategorie)
- `GET /api/categories/` - Lista wszystkich kategorii
- `POST /api/categories/` - Utworzenie nowej kategorii
- `GET /api/categories/{id}/` - Szczegóły kategorii
- `PUT /api/categories/{id}/` - Aktualizacja kategorii
- `DELETE /api/categories/{id}/` - Usunięcie kategorii
- `GET /api/categories/search/?name={tekst}` - Wyszukiwanie kategorii po nazwie

### Topic (Tematy)
- `GET /api/topics/` - Lista wszystkich tematów
- `POST /api/topics/` - Utworzenie nowego tematu
- `GET /api/topics/{id}/` - Szczegóły tematu
- `PUT /api/topics/{id}/` - Aktualizacja tematu
- `DELETE /api/topics/{id}/` - Usunięcie tematu
- `GET /api/topics/search/?name={tekst}` - Wyszukiwanie tematów po nazwie

### Post (Posty)
- `GET /api/posts/` - Lista wszystkich postów
- `POST /api/posts/` - Utworzenie nowego posta
- `GET /api/posts/{id}/` - Szczegóły posta
- `PUT /api/posts/{id}/` - Aktualizacja posta
- `DELETE /api/posts/{id}/` - Usunięcie posta
- `GET /api/posts/search/?name={tekst}` - Wyszukiwanie postów po tytule

---

## Przykłady użycia z curl

### 1. Przygotowanie - utworzenie kategorii i tematu

```bash
# Utworzenie kategorii
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technologia",
    "description": "Artykuły o technologii"
  }'

# Utworzenie tematu
curl -X POST http://localhost:8000/api/topics/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python i Django",
    "content": "Wszystko o frameworku Django",
    "category": 1
  }'
```

### 2. Dodanie dwóch nowych postów

**Post 1 - z prawidłowym tytułem (tylko litery):**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mój pierwszy artykuł",
    "text": "To jest treść mojego pierwszego artykułu o Django. Django jest świetnym frameworkiem do tworzenia aplikacji webowych.",
    "slug": "moj-pierwszy-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

**Post 2 - z eksperymentowaniem z datą:**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analiza danych w Pythonie",
    "text": "Python oferuje wiele bibliotek do analizy danych takich jak Pandas NumPy i Matplotlib.",
    "slug": "analiza-danych",
    "topic": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }'
```

**Post 3 - eksperyment z nieprawidłowym tytułem (zawiera cyfry - powinien zwrócić błąd):**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 3.11 nowości",
    "text": "Nowości w Python 3.11",
    "slug": "python-311",
    "topic": 1,
    "created_by": 1
  }'
# Oczekiwany błąd: "Tytuł może zawierać tylko litery i spacje"
```

**Post 4 - eksperyment z datą z przyszłości (powinien zwrócić błąd):**

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Przyszły artykuł",
    "text": "Treść artykułu z przyszłości",
    "slug": "przyszly-artykul",
    "topic": 1,
    "created_by": 1,
    "created_at": "2026-12-31T23:59:59Z"
  }'
# Oczekiwany błąd: "Data utworzenia nie może być z przyszłości"
```

### 3. Wyświetlenie wszystkich postów

```bash
curl -X GET http://localhost:8000/api/posts/
```

### 4. Modyfikacja posta (aktualizacja ID=1)

```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mój zaktualizowany artykuł",
    "text": "To jest zaktualizowana treść artykułu. Dodałem więcej informacji o Django REST Framework.",
    "slug": "moj-zaktualizowany-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

### 5. Usunięcie posta (ID=2)

```bash
curl -X DELETE http://localhost:8000/api/posts/2/
```

### 6. Wyświetlenie postów zawierających literę 'a' w nazwie

```bash
curl -X GET "http://localhost:8000/api/posts/search/?name=a"
```

Lub bardziej specyficzne wyszukiwanie:

```bash
# Wyszukiwanie postów z "artykuł" w tytule
curl -X GET "http://localhost:8000/api/posts/search/?name=artykuł"
```

---

## Przykłady dla innych encji

### Wyszukiwanie kategorii

```bash
# Wszystkie kategorie zawierające "tech" w nazwie
curl -X GET "http://localhost:8000/api/categories/search/?name=tech"
```

### Wyszukiwanie tematów

```bash
# Wszystkie tematy zawierające "python" w tytule
curl -X GET "http://localhost:8000/api/topics/search/?name=python"
```

### Szczegóły pojedynczej kategorii

```bash
curl -X GET http://localhost:8000/api/categories/1/
```

### Aktualizacja kategorii

```bash
curl -X PUT http://localhost:8000/api/categories/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technologia IT",
    "description": "Artykuły o technologii informatycznej"
  }'
```

### Usunięcie kategorii

```bash
curl -X DELETE http://localhost:8000/api/categories/1/
```

---

## Przykłady użycia z Postman

### Konfiguracja ogólna

1. Otwórz Postman
2. Ustaw **Base URL**: `http://localhost:8000/api/`
3. W zakładce Headers dodaj:
   - `Content-Type: application/json`

### Utworzenie nowego posta

1. Metoda: **POST**
2. URL: `http://localhost:8000/api/posts/`
3. Body → raw → JSON:
```json
{
  "title": "Mój post z Postmana",
  "text": "To jest treść posta utworzonego przez Postman",
  "slug": "post-z-postmana",
  "topic": 1,
  "created_by": 1
}
```
4. Kliknij **Send**

### Pobranie listy postów z filtrowaniem

1. Metoda: **GET**
2. URL: `http://localhost:8000/api/posts/search/`
3. Params:
   - Key: `name`
   - Value: `a`
4. Kliknij **Send**

### Aktualizacja posta

1. Metoda: **PUT**
2. URL: `http://localhost:8000/api/posts/1/`
3. Body → raw → JSON:
```json
{
  "title": "Zaktualizowany tytuł",
  "text": "Zaktualizowana treść",
  "slug": "zaktualizowany-tytul",
  "topic": 1,
  "created_by": 1
}
```
4. Kliknij **Send**

### Usunięcie posta

1. Metoda: **DELETE**
2. URL: `http://localhost:8000/api/posts/2/`
3. Kliknij **Send**
4. Powinieneś otrzymać status **204 No Content**

---

## Testowanie walidacji

### Test 1: Tytuł z cyframi (błąd)

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 3 tutorial",
    "text": "Treść",
    "slug": "python-3",
    "topic": 1,
    "created_by": 1
  }'
```

**Oczekiwany rezultat:**
```json
{
  "title": ["Tytuł może zawierać tylko litery i spacje (bez cyfr i znaków specjalnych)."]
}
```

### Test 2: Data z przyszłości (błąd)

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Przyszły post",
    "text": "Treść",
    "slug": "przyszly",
    "topic": 1,
    "created_by": 1,
    "created_at": "2030-01-01T00:00:00Z"
  }'
```

**Oczekiwany rezultat:**
```json
{
  "created_at": ["Data utworzenia nie może być z przyszłości."]
}
```

### Test 3: Prawidłowy tytuł tylko z literami

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Świetny artykuł o Django",
    "text": "To jest treść artykułu",
    "slug": "swietny-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

**Oczekiwany rezultat:** Status 201 Created z danymi utworzonego posta.

---

## Notatki

1. **Walidacja title**: Tytuł posta może zawierać tylko litery (w tym polskie znaki diakrytyczne) i spacje.
2. **Walidacja created_at**: Data utworzenia nie może być z przyszłości.
3. **ID użytkownika**: Upewnij się, że `created_by` wskazuje na istniejącego użytkownika.
4. **ID kategorii/tematu**: Upewnij się, że referencje (`category`, `topic`) wskazują na istniejące obiekty.
5. **Format daty**: Użyj formatu ISO 8601, np. `2024-01-15T10:30:00Z`

## Diagnostyka problemów

### Problem: 404 Not Found
- Sprawdź czy serwer działa: `python manage.py runserver`
- Sprawdź czy URL jest poprawny (uwzględnij `/api/` prefix)

### Problem: 400 Bad Request
- Sprawdź format JSON (czy jest poprawny)
- Sprawdź czy wszystkie wymagane pola są podane
- Sprawdź walidacje pól

### Problem: 500 Internal Server Error
- Sprawdź logi serwera Django
- Sprawdź czy migracje są wykonane: `python manage.py migrate`
- Sprawdź czy istnieją wymagane obiekty (kategorie, tematy, użytkownicy)
