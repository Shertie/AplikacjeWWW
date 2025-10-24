# Blog Django - Projekt na zajęcia

Projekt Django stworzony na zajęcia z Aplikacji WWW.

## Struktura projektu

```bash
AplikacjeWWW/
├── blog/                   # Główny katalog projektu Django
│   ├── blog/              # Konfiguracja projektu
│   │   ├── settings.py    # Ustawienia projektu
│   │   ├── urls.py        # Główne URLe
│   │   └── ...
│   ├── posts/             # Aplikacja posts
│   │   ├── models.py      # Modele Category, Topic, Post
│   │   ├── admin.py       # Konfiguracja panelu admin
│   │   ├── serializers.py # Serializatory DRF
│   │   ├── docs/          # Dokumentacja i testy
│   │   ├── migrations/    # Migracje bazy danych
│   │   └── ...
│   ├── manage.py          # Skrypt zarządzania Django
│   └── db.sqlite3         # Baza danych SQLite
└── .venv/                 # Środowisko wirtualne Python
```

## Modele

### Category

- `name` (CharField) - Nazwa kategorii (unikalna)
- `description` (TextField) - Opis kategorii
- `created_at` (DateTimeField) - Data utworzenia

### Topic

- `title` (CharField) - Tytuł tematu
- `content` (TextField) - Treść tematu
- `category` (ForeignKey) - Powiązanie z kategorią
- `created_at` (DateTimeField) - Data utworzenia
- `updated_at` (DateTimeField) - Data ostatniej modyfikacji

### Post

- `title` (CharField) - Tytuł posta (max 150 znaków)
- `text` (TextField) - Treść posta
- `topic` (ForeignKey) - Powiązanie z tematem
- `slug` (SlugField) - Slug URL
- `created_at` (DateTimeField) - Data utworzenia
- `updated_at` (DateTimeField) - Data ostatniej modyfikacji
- `created_by` (ForeignKey) - Autor posta (User)

## Django REST Framework

Projekt wykorzystuje Django REST Framework do tworzenia API.

### Serializatory

W pliku `posts/serializers.py` znajdują się:

1. **CategorySerializer** - serializator dziedziczący po `serializers.Serializer`
   - Ręczna implementacja wszystkich metod (create, update)
   - Walidacja formatowania nazwy (Title Case)
   - Sprawdzanie unikalności nazwy

2. **TopicSerializer** - serializator dziedziczący po `serializers.ModelSerializer`
   - Automatyczne generowanie pól z modelu
   - Zagnieżdżone dane kategorii
   - Pole `posts_count` (SerializerMethodField)

3. **PostSerializer** - serializator dla modelu Post
   - Automatyczne przypisywanie autora z kontekstu request
   - Walidacja i formatowanie tekstu
   - Zagnieżdżone informacje o topic, category i autorze

4. **PostListSerializer** - uproszczony serializator dla listy postów
   - Zawiera tylko podstawowe informacje
   - Pole `preview` z pierwszymi 5 wyrazami tekstu

### Testowanie serializatorów

Dokumentacja i testy znajdują się w folderze `posts/docs/`:

- `drf_serializer_test.md` - szczegółowa dokumentacja z przykładami użycia
- `test_serializers.py` - skrypt testowy do uruchomienia w Django shell

Uruchomienie testów:

```bash
cd blog
python manage.py shell < ./posts/docs/test_serializers.py
```

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone <url-repozytorium>
cd AplikacjeWWW
```

2. Utwórz i aktywuj środowisko wirtualne:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

3. Zainstaluj zależności:

```bash
pip install -r requirements.txt
# lub ręcznie:
pip install django django-debug-toolbar djangorestframework
```

4. Przejdź do katalogu projektu i wykonaj migracje:

```bash
cd blog
python manage.py migrate
```

5. Utwórz superusera:

```bash
python manage.py createsuperuser
```

6. Uruchom serwer deweloperski:

```bash
python manage.py runserver
```

7. Otwórz przeglądarkę i przejdź do:

- Panel administracyjny: <http://127.0.0.1:8000/admin/>
- Aplikacja: <http://127.0.0.1:8000/>

## Django Debug Toolbar

Projekt ma zainstalowany i skonfigurowany `django-debug-toolbar`. Toolbar pojawia się automatycznie na stronach gdy `DEBUG=True`.

### Funkcje Debug Toolbar

- Historia zapytań SQL
- Informacje o cache
- Czasy renderowania szablonów
- Nagłówki HTTP
- Profil wydajności
- Ustawienia projektu

## Wykonane zadania

### Lab 1-2

1. ✅ Utworzenie modeli Category i Topic
2. ✅ Dodanie pola description do modelu Category
3. ✅ Wykonanie migracji (makemigrations i migrate)
4. ✅ Testowanie wycofywania migracji (migrate posts 0001_initial)
5. ✅ Instalacja i konfiguracja django-debug-toolbar
6. ✅ Rejestracja modeli w panelu administracyjnym

### Lab 3

1. ✅ Utworzenie modelu Post z wszystkimi wymaganymi polami
2. ✅ Rejestracja modelu Post w admin z readonly_fields
3. ✅ Przesłonięcie metod `__str__()` dla wszystkich modeli
4. ✅ Dodanie Meta ordering dla wszystkich modeli
5. ✅ Konfiguracja list_display w ModelAdmin
6. ✅ Kolumna Topic z formatem "nazwa (kategoria)" używając @admin.display
7. ✅ Dodanie filtrów dla modeli
8. ✅ Automatyczne generowanie slug z prepopulated_fields
9. ✅ Zapytania Django QuerySet (lab_3_zadanie_10.md)

### Lab 4

1. ✅ Instalacja djangorestframework
2. ✅ Konfiguracja DRF w settings.py
3. ✅ Utworzenie CategorySerializer (serializers.Serializer)
4. ✅ Utworzenie TopicSerializer, PostSerializer (ModelSerializer)
5. ✅ Dokumentacja i testy serializatorów (posts/docs/)
6. ✅ Nadpisanie metod create/update z walidacją

## Użyteczne komendy

### Migracje

```bash
# Tworzenie migracji
python manage.py makemigrations

# Wykonywanie migracji
python manage.py migrate

# Wyświetlanie statusu migracji
python manage.py showmigrations

# Wycofywanie migracji
python manage.py migrate <app_name> <migration_name>
```

### Panel administracyjny

```bash
# Tworzenie superusera
python manage.py createsuperuser
```

### Serwer deweloperski

```bash
# Uruchamianie serwera
python manage.py runserver

# Uruchamianie na innym porcie
python manage.py runserver 8080
```

## Autor

Projekt wykonany na zajęcia z Aplikacji WWW.

## Licencja

Projekt edukacyjny - brak licencji.
