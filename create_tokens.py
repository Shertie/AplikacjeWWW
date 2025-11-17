#!/usr/bin/env python
"""
Skrypt do tworzenia tokenów dla istniejących użytkowników.
LAB 6 - Zadanie 3
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/fernis/Desktop/Projekty/Studia/AplikacjeWWW/blog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_tokens_for_all_users():
    """Tworzy tokeny dla wszystkich użytkowników, którzy ich nie mają."""
    users = User.objects.all()
    
    if not users.exists():
        print("Brak użytkowników w systemie!")
        print("Utwórz użytkownika: python manage.py createsuperuser")
        return
    
    print(f"Znaleziono {users.count()} użytkowników:\n")
    
    for user in users:
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print(f"✓ Utworzono nowy token dla użytkownika: {user.username}")
        else:
            print(f"○ Token już istnieje dla użytkownika: {user.username}")
        print(f"  Token: {token.key}")
        print(f"  User ID: {user.id}")
        print()

if __name__ == '__main__':
    print("=" * 60)
    print("TWORZENIE TOKENÓW DLA UŻYTKOWNIKÓW")
    print("=" * 60)
    print()
    create_tokens_for_all_users()
    print("=" * 60)
    print("Tokeny zostały wygenerowane!")
    print("Użyj tokenu w nagłówku: Authorization: Token <token_value>")
    print("=" * 60)
