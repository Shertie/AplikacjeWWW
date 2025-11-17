# Lab 6 - Autentykacja w Django i DRF - Podsumowanie

## Cel laboratorium

Implementacja różnych metod autentykacji w Django REST Framework:
- Autentykacja przez sesję (Session Authentication)
- Autentykacja Basic (Basic Authentication)
- Autentykacja tokenem (Token Authentication)

## Zrealizowane zadania

### ✅ Zadanie 1: Interfejs logowania DRF

**Implementacja:**
- Dodano endpoint `/api-auth/` w głównym pliku URLs (`blog/urls.py`)
- Umożliwia logowanie przez interfejs webowy DRF

**Kod:**
```python
# blog/urls.py
urlpatterns = [
    # ...
    path('api-auth/', include('rest_framework.urls')),
]
```

**Test:**
1. Otwórz przeglądarkę: `http://localhost:8001/api-auth/login/`
2. Zaloguj się danymi:
   - Username: `testuser`
   - Password: `testpass123`
3. Po zalogowaniu masz dostęp do chronionych endpointów przez interfejs DRF

---

### ✅ Zadanie 2: Endpoint dla postów zalogowanego użytkownika

**Endpoint:** `GET /api/users/posts/`

**Implementacja:**
```python
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_posts_list(request):
    """
    Zwraca listę postów utworzonych przez aktualnie zalogowanego użytkownika.
    """
    posts = Post.objects.filter(
        created_by=request.user
    ).select_related('topic', 'topic__category', 'created_by')
    
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
```

**Funkcjonalność:**
- Wymaga uwierzytelnienia (Session lub Basic Auth)
- Zwraca tylko posty utworzone przez zalogowanego użytkownika
- Bez logowania zwraca `403 Forbidden`

**Test:**
```bash
# Bez autentykacji - błąd 403
curl http://localhost:8001/api/users/posts/

# Z Basic Auth - sukces
curl -u testuser:testpass123 http://localhost:8001/api/users/posts/
```

---

### ✅ Zadanie 3: Autentykacja tokenem

**Implementacja:**

1. **Dodanie `rest_framework.authtoken` do INSTALLED_APPS:**
```python
# blog/settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',
    # ...
]
```

2. **Wykonanie migracji:**
```bash
python manage.py migrate
```

3. **Utworzenie tokenów dla użytkowników:**

Przygotowano skrypt `setup_test_user.py` który:
- Tworzy użytkownika testowego
- Generuje token dla użytkownika
- Wyświetla dane do logowania

**Token dla testuser:**
```
f5af0855508e5f5da2e35dee08ad44278c873258
```

**Użycie tokenu:**
```bash
# W curl
curl -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258" \
  http://localhost:8001/api/posts/

# W Postman
# Header: Authorization
# Value: Token f5af0855508e5f5da2e35dee08ad44278c873258
```

---

### ✅ Zadanie 4: Osobne endpointy PUT i DELETE z różnymi metodami autentykacji

**Endpointy:**
- `PUT /api/posts/update/<pk>/` - Session/Basic Auth
- `DELETE /api/posts/delete/<pk>/` - Token Auth

**Implementacja PUT (Session/Basic Auth):**
```python
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    """Aktualizacja posta - wymaga Session lub Basic Auth."""
    try:
        post = Post.objects.select_related(
            'topic', 'topic__category', 'created_by'
        ).get(pk=pk)
    except Post.DoesNotExist:
        raise Http404
    
    serializer = PostSerializer(post, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Implementacja DELETE (Token Auth):**
```python
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    """Usunięcie posta - wymaga Token Auth."""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```

**Test PUT:**
```bash
curl -X PUT http://localhost:8001/api/posts/update/1/ \
  -u testuser:testpass123 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Zaktualizowany tytuł",
    "text": "Nowa treść",
    "slug": "slug",
    "topic": 2,
    "created_by": 1
  }'
```

**Test DELETE:**
```bash
# Bez tokenu - błąd 401
curl -X DELETE http://localhost:8001/api/posts/delete/3/

# Z tokenem - sukces 204
curl -X DELETE http://localhost:8001/api/posts/delete/3/ \
  -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258"
```

---

### ✅ Zadanie 5: Topics dla kategorii (tylko Token Auth)

**Endpoint:** `GET /api/categories/<category_id>/topics/`

**Implementacja:**
```python
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_topics_list(request, category_id):
    """
    Zwraca listę wszystkich tematów dla podanej kategorii.
    Dostęp tylko do odczytu, wymaga Token Auth.
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    
    topics = Topic.objects.filter(category=category).select_related('category')
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)
```

**Funkcjonalność:**
- Wymaga **tylko** autentykacji tokenem
- Zwraca wszystkie tematy dla danej kategorii
- Dostęp tylko do odczytu (GET)

**Test:**
```bash
# Bez tokenu - błąd 401
curl http://localhost:8001/api/categories/2/topics/

# Z tokenem - sukces
curl -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258" \
  http://localhost:8001/api/categories/2/topics/
```

---

## Podsumowanie metod autentykacji

### 1. Session Authentication
- **Użycie:** Interfejs webowy DRF
- **Jak działa:** Bazuje na ciasteczkach sesji Django
- **Kiedy używać:** Dla aplikacji webowych z interfejsem DRF

### 2. Basic Authentication
- **Użycie:** `curl -u username:password`
- **Jak działa:** Wysyła username:password w nagłówku (base64)
- **Kiedy używać:** Do testowania, nie dla produkcji (bez szyfrowania)

### 3. Token Authentication
- **Użycie:** `curl -H "Authorization: Token <key>"`
- **Jak działa:** Każdy użytkownik ma unikalny token
- **Kiedy używać:** API dla aplikacji mobilnych/desktopowych

---

## Struktura plików

```
blog/
├── blog/
│   ├── settings.py          # Dodano 'rest_framework.authtoken'
│   └── urls.py              # Dodano 'api-auth/'
├── posts/
│   ├── views.py             # Dodano 4 nowe widoki z autentykacją
│   └── urls.py              # Dodano nowe endpointy
└── manage.py

Skrypty pomocnicze:
├── setup_test_user.py       # Tworzy użytkownika i token
├── create_test_data.py      # Tworzy dane testowe
├── create_tokens.py         # Generuje tokeny dla userów
└── test_lab6_auth.sh        # Automatyczne testy wszystkich zadań
```

---

## Nowe endpointy

| Endpoint | Metoda | Autentykacja | Opis |
|----------|--------|--------------|------|
| `/api-auth/login/` | GET | - | Interfejs logowania DRF |
| `/api/users/posts/` | GET | Session/Basic | Posty zalogowanego użytkownika |
| `/api/posts/update/<pk>/` | PUT | Session/Basic | Aktualizacja posta |
| `/api/posts/delete/<pk>/` | DELETE | Token | Usunięcie posta |
| `/api/categories/<id>/topics/` | GET | Token | Topics dla kategorii |

---

## Dane testowe

### Użytkownik
- **Username:** testuser
- **Password:** testpass123
- **Token:** f5af0855508e5f5da2e35dee08ad44278c873258
- **User ID:** 1

### Dane
- **Kategorie:** 2 (Programowanie, Technologia)
- **Topics:** 2 (Python i Django)
- **Posts:** 3 (utworzone przez testuser)

---

## Testowanie

### Automatyczny test
```bash
./test_lab6_auth.sh
```

Ten skrypt testuje wszystkie 5 zadań automatycznie.

### Testy ręczne

#### 1. Logowanie przez przeglądarkę
```
http://localhost:8001/api-auth/login/
```

#### 2. Posty użytkownika (Basic Auth)
```bash
curl -u testuser:testpass123 http://localhost:8001/api/users/posts/
```

#### 3. Pobieranie z tokenem
```bash
curl -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258" \
  http://localhost:8001/api/posts/
```

#### 4. Aktualizacja (Basic Auth)
```bash
curl -X PUT http://localhost:8001/api/posts/update/1/ \
  -u testuser:testpass123 \
  -H "Content-Type: application/json" \
  -d '{"title":"Nowy","text":"Treść","slug":"slug","topic":2,"created_by":1}'
```

#### 5. Usunięcie (Token)
```bash
curl -X DELETE http://localhost:8001/api/posts/delete/2/ \
  -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258"
```

#### 6. Topics kategorii (Token)
```bash
curl -H "Authorization: Token f5af0855508e5f5da2e35dee08ad44278c873258" \
  http://localhost:8001/api/categories/2/topics/
```

---

## Kody odpowiedzi HTTP

- **200 OK** - Sukces
- **201 Created** - Utworzono zasób
- **204 No Content** - Sukces (DELETE)
- **401 Unauthorized** - Brak autentykacji
- **403 Forbidden** - Brak uprawnień
- **404 Not Found** - Nie znaleziono zasobu

---

## Wnioski

✅ Wszystkie 5 zadań zostały zaimplementowane i przetestowane  
✅ API obsługuje 3 metody autentykacji  
✅ Różne endpointy mają różne wymagania autentykacyjne  
✅ Testy automatyczne potwierdzają poprawność implementacji  

## Dalsze możliwości

- **JWT (JSON Web Tokens)** - bardziej zaawansowana autentykacja
- **OAuth2** - autentykacja przez zewnętrzne serwisy
- **Permissions** - bardziej granularna kontrola dostępu
- **Throttling** - ograniczenie liczby zapytań
