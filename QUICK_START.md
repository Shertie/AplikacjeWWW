# Szybki Start - Laboratorium 5

## Krok 1: Uruchomienie serwera

```bash
cd blog
source ../.venv/bin/activate  # Aktywacja środowiska wirtualnego
python manage.py runserver
```

Serwer powinien być dostępny pod adresem: `http://127.0.0.1:8000/`

## Krok 2: Utworzenie użytkownika testowego (jeśli nie istnieje)

Otwórz nowy terminal i wykonaj:

```bash
cd blog
source ../.venv/bin/activate
python manage.py createsuperuser
```

Podaj dane:
- Username: `admin`
- Email: (możesz pominąć)
- Password: (wybierz hasło, np. `admin123`)

## Krok 3: Utworzenie danych testowych przez Django Admin

1. Przejdź do: `http://127.0.0.1:8000/admin/`
2. Zaloguj się jako `admin`
3. Utwórz Category:
   - Name: "Technologia"
   - Description: "Artykuły o technologii"
4. Utwórz Topic:
   - Title: "Python i Django"
   - Content: "Wszystko o frameworku Django"
   - Category: Wybierz "Technologia"

## Krok 4: Testowanie API

### Opcja A: Użyj skryptu automatycznego

```bash
cd ..  # Wróć do głównego katalogu projektu
./test_api.sh
```

### Opcja B: Testy ręczne z curl

#### 1. Dodaj nowy post:

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mój pierwszy artykuł",
    "text": "To jest treść mojego pierwszego artykułu o Django.",
    "slug": "moj-pierwszy-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

#### 2. Zobacz wszystkie posty:

```bash
curl -X GET http://localhost:8000/api/posts/
```

#### 3. Zaktualizuj post (ID=1):

```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Zaktualizowany artykuł",
    "text": "Zaktualizowana treść artykułu.",
    "slug": "zaktualizowany-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

#### 4. Wyszukaj posty z literą 'a':

```bash
curl -X GET "http://localhost:8000/api/posts/search/?name=a"
```

#### 5. Usuń post (ID=1):

```bash
curl -X DELETE http://localhost:8000/api/posts/1/
```

### Opcja C: Użyj przeglądarki (Django REST Framework)

Przejdź do:
- `http://127.0.0.1:8000/api/posts/` - Zobacz i dodaj posty
- `http://127.0.0.1:8000/api/categories/` - Zobacz i dodaj kategorie
- `http://127.0.0.1:8000/api/topics/` - Zobacz i dodaj tematy

### Opcja D: Użyj Postman

1. Otwórz Postman
2. Ustaw Base URL: `http://localhost:8000/api/`
3. Dodaj header: `Content-Type: application/json`
4. Wykonaj requesty zgodnie z dokumentacją w `API_DOCUMENTATION.md`

## Krok 5: Testowanie walidacji

### Test 1: Tytuł z cyframi (POWINIEN ZWRÓCIĆ BŁĄD)

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 3.11 nowości",
    "text": "Treść artykułu",
    "slug": "python-311",
    "topic": 1,
    "created_by": 1
  }'
```

Oczekiwany błąd: `"title": ["Tytuł może zawierać tylko litery i spacje..."]`

### Test 2: Data z przyszłości (POWINIEN ZWRÓCIĆ BŁĄD)

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Przyszły artykuł",
    "text": "Treść",
    "slug": "przyszly",
    "topic": 1,
    "created_by": 1,
    "created_at": "2026-12-31T23:59:59Z"
  }'
```

Oczekiwany błąd: `"created_at": ["Data utworzenia nie może być z przyszłości."]`

## Struktura endpointów

### Category
- `GET /api/categories/` - lista
- `POST /api/categories/` - dodaj
- `GET /api/categories/{id}/` - szczegóły
- `PUT /api/categories/{id}/` - aktualizuj
- `DELETE /api/categories/{id}/` - usuń
- `GET /api/categories/search/?name={tekst}` - szukaj

### Topic
- `GET /api/topics/` - lista
- `POST /api/topics/` - dodaj
- `GET /api/topics/{id}/` - szczegóły
- `PUT /api/topics/{id}/` - aktualizuj
- `DELETE /api/topics/{id}/` - usuń
- `GET /api/topics/search/?name={tekst}` - szukaj

### Post
- `GET /api/posts/` - lista
- `POST /api/posts/` - dodaj
- `GET /api/posts/{id}/` - szczegóły
- `PUT /api/posts/{id}/` - aktualizuj
- `DELETE /api/posts/{id}/` - usuń
- `GET /api/posts/search/?name={tekst}` - szukaj

## Rozwiązywanie problemów

### Błąd: Connection refused
→ Sprawdź czy serwer działa: `python manage.py runserver`

### Błąd: 404 Not Found
→ Sprawdź czy URL zawiera `/api/` prefix: `http://localhost:8000/api/posts/`

### Błąd: IntegrityError / ForeignKey
→ Upewnij się, że istnieją:
- Użytkownik o ID=1 (utwórz przez `createsuperuser`)
- Kategoria o ID=1
- Topic o ID=1

### Błąd: Walidacja nie działa
→ Sprawdź czy w `posts/serializers.py` pole `created_at` NIE jest w `read_only_fields`

## Więcej informacji

- Szczegółowa dokumentacja: `API_DOCUMENTATION.md`
- Podsumowanie zadań: `LAB5_SUMMARY.md`
- Skrypt testowy: `test_api.sh`
