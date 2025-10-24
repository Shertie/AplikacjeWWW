#!/usr/bin/env python
"""
Skrypt testowy dla serializatorów Django REST Framework.
Może być uruchomiony jako potok wejściowy do Django shell:
    python manage.py shell < ./posts/docs/test_serializers.py
"""

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
else:
    print("✗ Brak kategorii w bazie danych")

# Test aktualizacji
print("\n3. Aktualizacja kategorii:")
if Category.objects.exists():
    category_to_update = Category.objects.first()
    update_data = {
        'name': 'ZAKTUALIZOWANA nazwa',
        'description': 'Zaktualizowany opis'
    }
    update_serializer = CategorySerializer(category_to_update, data=update_data)
    if update_serializer.is_valid():
        updated = update_serializer.save()
        print(f"✓ Zaktualizowano: {updated.name}")
    else:
        print(f"✗ Błędy: {update_serializer.errors}")

# Test walidacji formatowania
print("\n4. Test formatowania nazwy:")
format_test_data = {
    'name': '  programowanie   w   pythonie  ',
    'description': 'Test formatowania'
}
format_serializer = CategorySerializer(data=format_test_data)
if format_serializer.is_valid():
    print(f"  Przed: '{format_test_data['name']}'")
    print(f"  Po:    '{format_serializer.validated_data['name']}'")
    formatted_category = format_serializer.save()
    print(f"✓ Zapisano jako: '{formatted_category.name}'")
else:
    print(f"✗ Błędy: {format_serializer.errors}")

print("\n" + "=" * 60)
print("TEST 2: TopicSerializer (serializers.ModelSerializer)")
print("=" * 60)

# Test tworzenia tematu
print("\n1. Tworzenie nowego tematu:")
if Category.objects.exists():
    first_category = Category.objects.first()
    topic_data = {
        'title': '   test   formatowania   tytułu   ',
        'content': 'Treść testowego tematu z wieloma liniami.\n\nTo jest druga linia.\nI trzecia linia.',
        'category': first_category.id
    }
    
    topic_serializer = TopicSerializer(data=topic_data)
    if topic_serializer.is_valid():
        topic = topic_serializer.save()
        print(f"✓ Utworzono: {topic.title}")
        print(f"  Formatowanie tytułu: '{topic_data['title'].strip()}' → '{topic.title}'")
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
    if serializer.data.get('category_detail'):
        print(f"  Szczegóły kategorii:")
        print(f"    - Nazwa: {serializer.data['category_detail']['name']}")
        print(f"    - Opis: {serializer.data['category_detail']['description']}")
else:
    print("✗ Brak tematów w bazie danych")

# Test serializacji wielu obiektów
print("\n3. Serializacja wielu obiektów:")
topics = Topic.objects.all()[:5]
if topics.exists():
    serializer = TopicSerializer(topics, many=True)
    print(f"✓ Zserializowano {len(serializer.data)} tematów:")
    for t in serializer.data:
        print(f"  - {t['title']} ({t['category_name']}) - {t['posts_count']} postów")
else:
    print("✗ Brak tematów w bazie danych")

# Test częściowej aktualizacji
print("\n4. Częściowa aktualizacja tematu (partial=True):")
if Topic.objects.exists():
    topic_to_update = Topic.objects.first()
    partial_data = {
        'title': 'NOWY zaktualizowany tytuł'
    }
    partial_serializer = TopicSerializer(topic_to_update, data=partial_data, partial=True)
    if partial_serializer.is_valid():
        updated_topic = partial_serializer.save()
        print(f"✓ Zaktualizowano tytuł: {updated_topic.title}")
        print(f"  Kategoria pozostała: {updated_topic.category.name}")
        print(f"  Treść pozostała niezmieniona")
    else:
        print(f"✗ Błędy: {partial_serializer.errors}")

print("\n" + "=" * 60)
print("PODSUMOWANIE")
print("=" * 60)
print(f"Liczba kategorii w bazie: {Category.objects.count()}")
print(f"Liczba tematów w bazie: {Topic.objects.count()}")
print("\nTesty zakończone!")
print("=" * 60)
