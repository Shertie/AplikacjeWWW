#!/usr/bin/env python
"""
Skrypt do tworzenia testowego użytkownika i tokenu.
LAB 6 - Setup
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

def create_test_user():
    """Tworzy testowego użytkownika jeśli nie istnieje."""
    
    # Sprawdź czy użytkownik już istnieje
    if User.objects.filter(username='testuser').exists():
        user = User.objects.get(username='testuser')
        print(f"✓ Użytkownik 'testuser' już istnieje (ID: {user.id})")
    else:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✓ Utworzono użytkownika: testuser (ID: {user.id})")
    
    # Utwórz token dla użytkownika
    token, created = Token.objects.get_or_create(user=user)
    if created:
        print(f"✓ Utworzono nowy token")
    else:
        print(f"✓ Token już istnieje")
    
    print()
    print("=" * 60)
    print("DANE LOGOWANIA:")
    print("=" * 60)
    print(f"Username: testuser")
    print(f"Password: testpass123")
    print(f"Token:    {token.key}")
    print(f"User ID:  {user.id}")
    print("=" * 60)
    
    return user, token

if __name__ == '__main__':
    print("=" * 60)
    print("KONFIGURACJA TESTOWEGO UŻYTKOWNIKA")
    print("=" * 60)
    print()
    create_test_user()
