#!/usr/bin/env python
"""
Skrypt do tworzenia danych testowych dla LAB 6.
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/fernis/Desktop/Projekty/Studia/AplikacjeWWW/blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from posts.models import Category, Topic, Post
from django.utils import timezone

def create_test_data():
    """Tworzy dane testowe."""
    
    # Pobierz użytkownika
    user = User.objects.get(username='testuser')
    print(f"✓ Użytkownik: {user.username} (ID: {user.id})")
    
    # Utwórz kategorię
    category, created = Category.objects.get_or_create(
        name="Programowanie",
        defaults={'description': "Artykuły o programowaniu"}
    )
    if created:
        print(f"✓ Utworzono kategorię: {category.name} (ID: {category.id})")
    else:
        print(f"○ Kategoria już istnieje: {category.name} (ID: {category.id})")
    
    # Utwórz topic
    topic, created = Topic.objects.get_or_create(
        title="Python i Django",
        category=category,
        defaults={'content': "Framework Django do tworzenia aplikacji webowych"}
    )
    if created:
        print(f"✓ Utworzono topic: {topic.title} (ID: {topic.id})")
    else:
        print(f"○ Topic już istnieje: {topic.title} (ID: {topic.id})")
    
    # Utwórz kilka postów
    posts_data = [
        {
            'title': 'Wprowadzenie do Django',
            'text': 'Django to potężny framework webowy napisany w Pythonie. Pozwala na szybkie tworzenie aplikacji.',
            'slug': 'wprowadzenie-do-django',
        },
        {
            'title': 'REST API w Django',
            'text': 'Django REST Framework ułatwia tworzenie API. Zapewnia wiele gotowych komponentów.',
            'slug': 'rest-api-django',
        },
        {
            'title': 'Autentykacja w DRF',
            'text': 'DRF oferuje różne metody autentykacji: sesję, token, JWT i inne.',
            'slug': 'autentykacja-drf',
        }
    ]
    
    print()
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'text': post_data['text'],
                'topic': topic,
                'created_by': user,
            }
        )
        if created:
            print(f"✓ Utworzono post: {post.title} (ID: {post.id})")
        else:
            print(f"○ Post już istnieje: {post.title} (ID: {post.id})")
    
    print()
    print("=" * 60)
    print("PODSUMOWANIE DANYCH TESTOWYCH:")
    print("=" * 60)
    print(f"Kategorie: {Category.objects.count()}")
    print(f"Topici:    {Topic.objects.count()}")
    print(f"Posty:     {Post.objects.count()}")
    print(f"  - Użytkownika 'testuser': {Post.objects.filter(created_by=user).count()}")
    print("=" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("TWORZENIE DANYCH TESTOWYCH")
    print("=" * 60)
    print()
    create_test_data()
