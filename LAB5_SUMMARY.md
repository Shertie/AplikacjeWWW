# Laboratorium 5 - REST API dla aplikacji Blog

## Zrealizowane zadania

### 1. Walidacja pól dla klasy Post

#### Walidacja pola `title` (nazwa)
- **Wymóg**: Może zawierać tylko litery
- **Implementacja**: W pliku `posts/serializers.py`, metoda `validate_title()` w klasie `PostSerializer`
- **Regex**: `^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]+$` (obsługa polskich znaków)
- **Komunikat błędu**: "Tytuł może zawierać tylko litery i spacje (bez cyfr i znaków specjalnych)."

#### Walidacja pola `created_at` (data_dodania)
- **Wymóg**: Nie może być z przyszłości
- **Implementacja**: W pliku `posts/serializers.py`, metoda `validate_created_at()` w klasie `PostSerializer`
- **Logika**: Porównanie z `timezone.now()`
- **Komunikat błędu**: "Data utworzenia nie może być z przyszłości."
- **Uwaga**: Pole `created_at` zostało usunięte z `read_only_fields` aby umożliwić walidację

### 2. Przygotowane endpointy API

Wszystkie endpointy są dostępne pod prefiksem `/api/`.

#### Endpointy dla Category:
- `GET /api/categories/` - Lista wszystkich kategorii
- `POST /api/categories/` - Dodanie nowej kategorii
- `GET /api/categories/{id}/` - Wyświetlanie szczegółów kategorii
- `PUT /api/categories/{id}/` - Aktualizacja kategorii
- `DELETE /api/categories/{id}/` - Usuwanie kategorii
- `GET /api/categories/search/?name={tekst}` - Wyszukiwanie kategorii po nazwie

#### Endpointy dla Topic:
- `GET /api/topics/` - Lista wszystkich tematów
- `POST /api/topics/` - Dodanie nowego tematu
- `GET /api/topics/{id}/` - Wyświetlanie szczegółów tematu
- `PUT /api/topics/{id}/` - Aktualizacja tematu
- `DELETE /api/topics/{id}/` - Usuwanie tematu
- `GET /api/topics/search/?name={tekst}` - Wyszukiwanie tematów po tytule

#### Endpointy dla Post:
- `GET /api/posts/` - Lista wszystkich postów
- `POST /api/posts/` - Dodanie nowego posta
- `GET /api/posts/{id}/` - Wyświetlanie szczegółów posta
- `PUT /api/posts/{id}/` - Aktualizacja posta
- `DELETE /api/posts/{id}/` - Usuwanie posta
- `GET /api/posts/search/?name={tekst}` - Wyszukiwanie postów po tytule

### 3. Przykłady użycia API

#### Przygotowanie środowiska

Przed wykonaniem testów:
1. Uruchom serwer Django: `python manage.py runserver`
2. Upewnij się, że masz utworzonego użytkownika (ID=1)
3. Utwórz kategorię i temat do testowania postów

#### Sposób 1: Automatyczny skrypt testowy

Przygotowany skrypt bash `test_api.sh` wykonuje wszystkie wymagane operacje:

```bash
chmod +x test_api.sh
./test_api.sh
```

Skrypt testuje:
- Dodanie 2 nowych postów (z różnymi parametrami)
- Walidację (tytuł z cyframi, data z przyszłości)
- Modyfikację posta
- Usunięcie posta
- Wyszukiwanie postów z literą 'a' w nazwie

#### Sposób 2: Ręczne testy z curl

##### a) Dodanie dwóch nowych postów

**Post 1 - prawidłowy:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mój pierwszy artykuł o Django",
    "text": "Django to potężny framework Pythona do tworzenia aplikacji webowych.",
    "slug": "moj-pierwszy-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

**Post 2 - z datą z przeszłości:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analiza danych w Python",
    "text": "Python oferuje wiele bibliotek do analizy danych.",
    "slug": "analiza-danych",
    "topic": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }'
```

##### b) Modyfikacja posta

```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Zaktualizowany artykuł o Django",
    "text": "Django to świetny framework który został zaktualizowany.",
    "slug": "zaktualizowany-artykul",
    "topic": 1,
    "created_by": 1
  }'
```

##### c) Usunięcie posta

```bash
curl -X DELETE http://localhost:8000/api/posts/2/
```

##### d) Wyświetlenie postów zawierających literę 'a'

```bash
curl -X GET "http://localhost:8000/api/posts/search/?name=a"
```

#### Sposób 3: Postman

1. Zaimportuj collection lub ręcznie utwórz requesty
2. Ustaw Base URL: `http://localhost:8000/api/`
3. Ustaw Header: `Content-Type: application/json`
4. Wykonaj operacje zgodnie z przykładami w dokumentacji

#### Sposób 4: Django REST Framework Browsable API

Przejdź w przeglądarce do:
- `http://localhost:8000/api/posts/` - Lista postów z formularzem do dodawania
- `http://localhost:8000/api/posts/1/` - Szczegóły posta z formularzem do edycji
- `http://localhost:8000/api/posts/search/?name=a` - Wyszukiwanie

### 4. Testowanie walidacji

#### Test 1: Tytuł z cyframi (BŁĄD)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 3.11 nowości",
    "text": "Treść",
    "slug": "python-311",
    "topic": 1,
    "created_by": 1
  }'
```
**Oczekiwany wynik:** Błąd walidacji - "Tytuł może zawierać tylko litery..."

#### Test 2: Data z przyszłości (BŁĄD)
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
**Oczekiwany wynik:** Błąd walidacji - "Data utworzenia nie może być z przyszłości."

## Struktura plików

```
blog/
├── posts/
│   ├── models.py          # Modele: Category, Topic, Post
│   ├── serializers.py     # Serializatory z walidacją
│   ├── views.py           # Widoki API (APIView)
│   └── urls.py            # URLe dla endpointów posts
├── blog/
│   ├── settings.py        # Dodano 'rest_framework' do INSTALLED_APPS
│   └── urls.py            # Dodano include('posts.urls')
└── manage.py

API_DOCUMENTATION.md       # Szczegółowa dokumentacja API
test_api.sh               # Skrypt automatycznych testów
```

## Zaimplementowane funkcje

1. ✅ Walidacja pola `title` - tylko litery (z polskimi znakami)
2. ✅ Walidacja pola `created_at` - nie z przyszłości
3. ✅ Pełne CRUD dla Category (Create, Read, Update, Delete)
4. ✅ Pełne CRUD dla Topic
5. ✅ Pełne CRUD dla Post
6. ✅ Wyszukiwanie Category po nazwie
7. ✅ Wyszukiwanie Topic po tytule
8. ✅ Wyszukiwanie Post po tytule
9. ✅ Dokumentacja API z przykładami curl i Postman
10. ✅ Automatyczny skrypt testowy

## Dodatkowe informacje

- **Framework**: Django REST Framework
- **Architektura widoków**: APIView (klasowe widoki API)
- **Serializatory**: Mix Serializer i ModelSerializer
- **Walidacja**: Własne metody validate_* w serializatorach
- **Filtrowan ie**: Query parametry (icontains)
- **Dokumentacja**: API_DOCUMENTATION.md

## Użyte narzędzia

1. **curl** - testy z linii komend
2. **Postman** - testy GUI (opcjonalnie)
3. **Django REST Framework Browsable API** - interfejs webowy
4. **Bash script** - automatyczne testy (test_api.sh)
