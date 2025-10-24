# Django REST Framework - Testy Serializatorów

## Opis

Ten dokument zawiera przykłady użycia serializatorów dla aplikacji `posts`:

- **CategorySerializer** - serializator dziedziczący po `serializers.Serializer`
- **TopicSerializer** - serializator dziedziczący po `serializers.ModelSerializer`

## Przygotowanie środowiska

Aby przetestować serializatory, uruchom Django shell:

```bash
python manage.py shell
```

Lub użyj pliku jako potoku wejściowego:

```bash
python manage.py shell < ./posts/docs/test_serializers.py
```

## Test 1: CategorySerializer (serializers.Serializer)

CategorySerializer dziedziczy po `serializers.Serializer` i implementuje ręcznie wszystkie metody.

### Tworzenie nowej kategorii

```python
from posts.serializers import CategorySerializer
from posts.models import Category

# Dane wejściowe
data = {
    'name': 'technologia',
    'description': 'Artykuły o nowoczesnych technologiach'
}

# Utworzenie serializatora
serializer = CategorySerializer(data=data)

# Walidacja danych
if serializer.is_valid():
    print("Dane są poprawne!")
    print("Zwalidowane dane:", serializer.validated_data)
    
    # Zapisanie do bazy danych
    category = serializer.save()
    print(f"Utworzono kategorię: {category.name} (ID: {category.id})")
    print(f"Nazwa po walidacji (Title Case): {category.name}")
else:
    print("Błędy walidacji:", serializer.errors)

# Oczekiwany output:
# Dane są poprawne!
# Zwalidowane dane: {'name': 'Technologia', 'description': 'Artykuły o nowoczesnych technologiach'}
# Utworzono kategorię: Technologia (ID: 1)
# Nazwa po walidacji (Title Case): Technologia
```

### Serializacja istniejącej kategorii

```python
from posts.serializers import CategorySerializer
from posts.models import Category

# Pobierz istniejącą kategorię
category = Category.objects.first()

# Serializuj obiekt
serializer = CategorySerializer(category)

# Wyświetl zserializowane dane
print("Zserializowane dane:")
print(serializer.data)

# Oczekiwany output:
# Zserializowane dane:
# {'id': 1, 'name': 'Technologia', 'description': 'Artykuły o nowoczesnych technologiach', 'created_at': '2025-10-24T10:30:00Z'}
```

### Aktualizacja kategorii

```python
from posts.serializers import CategorySerializer
from posts.models import Category

# Pobierz kategorię do aktualizacji
category = Category.objects.get(id=1)

# Nowe dane
update_data = {
    'name': 'NAUKA I TECHNOLOGIA',
    'description': 'Zaktualizowany opis kategorii'
}

# Utwórz serializator z instancją do aktualizacji
serializer = CategorySerializer(category, data=update_data)

# Walidacja i zapis
if serializer.is_valid():
    updated_category = serializer.save()
    print(f"Zaktualizowano kategorię: {updated_category.name}")
    print(f"Nowy opis: {updated_category.description}")
else:
    print("Błędy:", serializer.errors)

# Oczekiwany output:
# Zaktualizowano kategorię: Nauka I Technologia
# Nowy opis: Zaktualizowany opis kategorii
```

### Test walidacji - duplikat nazwy

```python
from posts.serializers import CategorySerializer

# Próba utworzenia kategorii z istniejącą nazwą
duplicate_data = {
    'name': 'technologia',  # Ta nazwa już istnieje
    'description': 'Test duplikatu'
}

serializer = CategorySerializer(data=duplicate_data)

if serializer.is_valid():
    serializer.save()
else:
    print("Błąd walidacji (oczekiwany):")
    print(serializer.errors)

# Oczekiwany output:
# Błąd walidacji (oczekiwany):
# {'name': ['Kategoria o tej nazwie już istnieje.']}
```

### Test walidacji - formatowanie nazwy

```python
from posts.serializers import CategorySerializer

# Testowanie automatycznego formatowania
test_data = {
    'name': '  programowanie   w   pythonie  ',  # Nadmiarowe spacje
    'description': 'Test formatowania'
}

serializer = CategorySerializer(data=test_data)

if serializer.is_valid():
    print("Oryginalna nazwa:", test_data['name'])
    print("Po walidacji:", serializer.validated_data['name'])
    category = serializer.save()
    print(f"Zapisana nazwa: '{category.name}'")

# Oczekiwany output:
# Oryginalna nazwa:   programowanie   w   pythonie  
# Po walidacji: Programowanie W Pythonie
# Zapisana nazwa: 'Programowanie W Pythonie'
```

## Test 2: TopicSerializer (serializers.ModelSerializer)

TopicSerializer dziedziczy po `serializers.ModelSerializer` i wykorzystuje automatyczne generowanie pól.

### Tworzenie nowego tematu

```python
from posts.serializers import TopicSerializer
from posts.models import Category, Topic

# Najpierw upewnij się, że istnieje kategoria
category = Category.objects.first()

# Dane dla nowego tematu
topic_data = {
    'title': '   wprowadzenie do DJANGO   ',  # Test formatowania
    'content': 'Django to potężny framework webowy napisany w Pythonie.',
    'category': category.id
}

# Utworzenie serializatora
serializer = TopicSerializer(data=topic_data)

# Walidacja i zapis
if serializer.is_valid():
    print("Dane poprawne!")
    print("Tytuł po walidacji:", serializer.validated_data['title'])
    
    topic = serializer.save()
    print(f"Utworzono temat: {topic.title}")
    print(f"Przypisany do kategorii: {topic.category.name}")
else:
    print("Błędy:", serializer.errors)

# Oczekiwany output:
# Dane poprawne!
# Tytuł po walidacji: Wprowadzenie do django
# Utworzono temat: Wprowadzenie do django
# Przypisany do kategorii: Technologia
```

### Serializacja z zagnieżdżonymi danymi

```python
from posts.serializers import TopicSerializer
from posts.models import Topic

# Pobierz temat
topic = Topic.objects.first()

# Serializuj z zagnieżdżonymi danymi
serializer = TopicSerializer(topic)

print("Zserializowane dane z zagnieżdżeniem:")
print(serializer.data)

# Oczekiwany output:
# {
#     'id': 1,
#     'title': 'Wprowadzenie do django',
#     'content': 'Django to potężny framework webowy napisany w Pythonie.',
#     'category': 1,
#     'category_name': 'Technologia',
#     'category_detail': {
#         'id': 1,
#         'name': 'Technologia',
#         'description': 'Artykuły o nowoczesnych technologiach',
#         'created_at': '2025-10-24T10:30:00Z'
#     },
#     'posts_count': 0,
#     'created_at': '2025-10-24T11:00:00Z',
#     'updated_at': '2025-10-24T11:00:00Z'
# }
```

### Serializacja wielu obiektów

```python
from posts.serializers import TopicSerializer
from posts.models import Topic

# Pobierz wszystkie tematy
topics = Topic.objects.all()

# Serializuj listę obiektów (many=True)
serializer = TopicSerializer(topics, many=True)

print(f"Liczba tematów: {len(serializer.data)}")
print("Tytuły tematów:")
for topic_data in serializer.data:
    print(f"  - {topic_data['title']} (kategoria: {topic_data['category_name']})")

# Oczekiwany output:
# Liczba tematów: 3
# Tytuły tematów:
#   - Wprowadzenie do django (kategoria: Technologia)
#   - Python dla początkujących (kategoria: Programowanie)
#   - Sztuczna inteligencja (kategoria: Nauka)
```

### Test SerializerMethodField - posts_count

```python
from posts.serializers import TopicSerializer
from posts.models import Topic, Post, Category
from django.contrib.auth.models import User

# Utwórz użytkownika jeśli nie istnieje
user, created = User.objects.get_or_create(username='testuser')

# Utwórz kategorię i temat
category, _ = Category.objects.get_or_create(
    name='Test',
    defaults={'description': 'Kategoria testowa'}
)

topic, _ = Topic.objects.get_or_create(
    title='Temat testowy',
    category=category,
    defaults={'content': 'Treść testowa'}
)

# Dodaj kilka postów do tematu
for i in range(3):
    Post.objects.create(
        title=f'Post {i+1}',
        text=f'Treść posta {i+1}',
        topic=topic,
        slug=f'post-{i+1}',
        created_by=user
    )

# Serializuj temat
serializer = TopicSerializer(topic)
print(f"Temat: {serializer.data['title']}")
print(f"Liczba postów: {serializer.data['posts_count']}")

# Oczekiwany output:
# Temat: Temat testowy
# Liczba postów: 3
```

### Aktualizacja tematu

```python
from posts.serializers import TopicSerializer
from posts.models import Topic

# Pobierz temat do aktualizacji
topic = Topic.objects.first()

# Nowe dane
update_data = {
    'title': 'ZAKTUALIZOWANY tytuł',
    'content': 'Nowa treść po aktualizacji'
}

# Utwórz serializator z instancją (partial=True pozwala na częściową aktualizację)
serializer = TopicSerializer(topic, data=update_data, partial=True)

if serializer.is_valid():
    updated_topic = serializer.save()
    print(f"Zaktualizowano temat: {updated_topic.title}")
    print(f"Kategoria pozostała: {updated_topic.category.name}")
else:
    print("Błędy:", serializer.errors)

# Oczekiwany output:
# Zaktualizowano temat: Zaktualizowany tytuł
# Kategoria pozostała: Technologia
```

## Pełny skrypt testowy

Poniżej znajduje się kompletny skrypt, który można uruchomić jako potok wejściowy:

```python
# posts/docs/test_serializers.py

from posts.serializers import CategorySerializer, TopicSerializer
from posts.models import Category, Topic

print("=" * 60)
print("TEST 1: CategorySerializer (serializers.Serializer)")
print("=" * 60)

# Test tworzenia kategorii
print("\n1. Tworzenie nowej kategorii:")
category_data = {
    'name': 'nowa kategoria testowa',
    'description': 'Opis kategorii testowej'
}

category_serializer = CategorySerializer(data=category_data)
if category_serializer.is_valid():
    category = category_serializer.save()
    print(f"✓ Utworzono: {category.name} (ID: {category.id})")
    print(f"  Formatowanie: '{category_data['name']}' → '{category.name}'")
else:
    print(f"✗ Błędy: {category_serializer.errors}")

# Test serializacji
print("\n2. Serializacja istniejącej kategorii:")
existing_category = Category.objects.first()
if existing_category:
    serializer = CategorySerializer(existing_category)
    print(f"✓ Zserializowano kategorię:")
    for key, value in serializer.data.items():
        print(f"  {key}: {value}")

print("\n" + "=" * 60)
print("TEST 2: TopicSerializer (serializers.ModelSerializer)")
print("=" * 60)

# Test tworzenia tematu
print("\n1. Tworzenie nowego tematu:")
if Category.objects.exists():
    first_category = Category.objects.first()
    topic_data = {
        'title': '   test   formatowania   tytułu   ',
        'content': 'Treść testowego tematu.',
        'category': first_category.id
    }
    
    topic_serializer = TopicSerializer(data=topic_data)
    if topic_serializer.is_valid():
        topic = topic_serializer.save()
        print(f"✓ Utworzono: {topic.title}")
        print(f"  Formatowanie: '{topic_data['title'].strip()}' → '{topic.title}'")
        print(f"  Kategoria: {topic.category.name}")
    else:
        print(f"✗ Błędy: {topic_serializer.errors}")
else:
    print("✗ Brak kategorii w bazie danych")

# Test serializacji z zagnieżdżonymi danymi
print("\n2. Serializacja z zagnieżdżonymi danymi:")
if Topic.objects.exists():
    topic = Topic.objects.first()
    serializer = TopicSerializer(topic)
    print(f"✓ Temat: {serializer.data['title']}")
    print(f"  ID kategorii: {serializer.data['category']}")
    print(f"  Nazwa kategorii: {serializer.data['category_name']}")
    print(f"  Liczba postów: {serializer.data['posts_count']}")

# Test serializacji wielu obiektów
print("\n3. Serializacja wielu obiektów:")
topics = Topic.objects.all()[:3]
serializer = TopicSerializer(topics, many=True)
print(f"✓ Zserializowano {len(serializer.data)} tematów:")
for t in serializer.data:
    print(f"  - {t['title']} ({t['category_name']})")

print("\n" + "=" * 60)
print("Testy zakończone!")
print("=" * 60)
```

## Uruchamianie testów

### Metoda 1: Interaktywna w Django shell

```bash
cd blog
python manage.py shell
```

Następnie kopiuj i wklej kod z sekcji testowych.

### Metoda 2: Jako potok wejściowy

Zapisz pełny skrypt testowy w pliku `posts/docs/test_serializers.py`, a następnie uruchom:

```bash
cd blog
python manage.py shell < ./posts/docs/test_serializers.py
```

## Kluczowe różnice między serializatorami

### CategorySerializer (serializers.Serializer)

**Zalety:**

- Pełna kontrola nad każdym polem
- Możliwość niestandardowej walidacji
- Elastyczność w implementacji

**Wady:**

- Więcej kodu do napisania
- Ręczna implementacja create() i update()
- Trzeba ręcznie definiować wszystkie pola

**Kiedy używać:**

- Gdy potrzebujesz specjalnej logiki walidacji
- Gdy serializator nie mapuje 1:1 z modelem
- Gdy potrzebujesz pełnej kontroli nad procesem

### TopicSerializer (serializers.ModelSerializer)

**Zalety:**

- Automatyczne generowanie pól z modelu
- Wbudowane metody create() i update()
- Mniej kodu boilerplate
- Łatwe zagnieżdżanie innych serializatorów

**Wady:**

- Mniejsza elastyczność
- Czasem trzeba nadpisywać domyślne zachowanie

**Kiedy używać:**

- Gdy serializator mapuje bezpośrednio z modelu
- Dla standardowych operacji CRUD
- Gdy chcesz szybko utworzyć API

## Podsumowanie

Obydwa typy serializatorów mają swoje zastosowanie:

- **serializers.Serializer** - dla złożonych przypadków wymagających niestandardowej logiki
- **serializers.ModelSerializer** - dla standardowych operacji CRUD na modelach

W praktycznych aplikacjach często używa się kombinacji obu podejść, w zależności od konkretnych wymagań.
