# Blog Django - Projekt na zajęcia

Projekt Django stworzony na zajęcia z Aplikacji WWW.

## Struktura projektu

```
AplikacjeWWW/
├── blog/                   # Główny katalog projektu Django
│   ├── blog/              # Konfiguracja projektu
│   │   ├── settings.py    # Ustawienia projektu
│   │   ├── urls.py        # Główne URLe
│   │   └── ...
│   ├── posts/             # Aplikacja posts
│   │   ├── models.py      # Modele Category i Topic
│   │   ├── admin.py       # Konfiguracja panelu admin
│   │   ├── migrations/    # Migracje bazy danych
│   │   └── ...
│   ├── manage.py          # Skrypt zarządzania Django
│   └── db.sqlite3         # Baza danych SQLite
└── venv/                  # Środowisko wirtualne Python
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
   pip install django django-debug-toolbar
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

1. ✅ Utworzenie modeli Category i Topic
2. ✅ Dodanie pola description do modelu Category
3. ✅ Wykonanie migracji (makemigrations i migrate)
4. ✅ Testowanie wycofywania migracji (migrate posts 0001_initial)
5. ✅ Instalacja i konfiguracja django-debug-toolbar
6. ✅ Rejestracja modeli w panelu administracyjnym

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