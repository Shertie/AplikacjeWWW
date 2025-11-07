# Refaktoryzacja API - Django REST Framework Tutorial 3

## Cel zadania

Zamiana implementacji API dla modeli zgodnie z przykładem z dokumentacji Django REST Framework Tutorial 3: Class-based Views.

**Dokumentacja**: https://www.django-rest-framework.org/tutorial/3-class-based-views/

## Wprowadzone zmiany

### 1. Zmiana importów w `posts/views.py`

**Przed:**
```python
from django.shortcuts import get_object_or_404
```

**Po:**
```python
from django.http import Http404
```

**Powód**: Zgodnie z tutorialem DRF, używamy `Http404` zamiast `get_object_or_404` dla lepszej kontroli nad obsługą błędów w APIView.

### 2. Dodanie metody `get_object()` w DetailView

Zgodnie z wzorcem z dokumentacji, każda klasa DetailView (CategoryDetailView, TopicDetailView, PostDetailView) otrzymała metodę `get_object()`:

**Przykład dla PostDetailView:**

```python
class PostDetailView(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    
    def get_object(self, pk):
        """
        Pobierz post o podanym ID lub zwróć Http404.
        """
        try:
            return Post.objects.select_related(
                'topic', 'topic__category', 'created_by'
            ).get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """Pobierz post."""
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Zaktualizuj post."""
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Usuń post."""
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Zalety:**
- Centralizacja logiki pobierania obiektów
- Łatwiejsze testowanie
- Konsystentna obsługa błędów
- Zgodność z wzorcem DRF

### 3. Dodanie parametru `format=None`

Wszystkie metody HTTP (get, post, put, delete) w widokach APIView otrzymały parametr `format=None`:

**Przed:**
```python
def get(self, request, pk):
```

**Po:**
```python
def get(self, request, pk, format=None):
```

**Powód**: Umożliwia obsługę format suffixes (.json, .api, etc.)

### 4. Aktualizacja docstringów

Zmieniono docstringi z polskich opisów na angielskie zgodnie z konwencją DRF:

**Przed:**
```python
class PostListView(APIView):
    """
    GET: Wyświetlanie listy wszystkich postów.
    POST: Dodawanie nowego posta.
    """
```

**Po:**
```python
class PostListView(APIView):
    """
    List all posts, or create a new post.
    """
```

### 5. Dodanie `format_suffix_patterns` w URLs

**Plik: `posts/urls.py`**

**Dodano:**
```python
from rest_framework.urlpatterns import format_suffix_patterns

# ... definicje urlpatterns ...

# Dodanie obsługi format suffixes (.json, .api, etc.)
urlpatterns = format_suffix_patterns(urlpatterns)
```

**Efekt**: Teraz można używać różnych formatów w URL:
- `http://localhost:8000/api/posts/` - domyślny format
- `http://localhost:8000/api/posts.json` - format JSON
- `http://localhost:8000/api/posts/1.json` - pojedynczy obiekt w JSON

## Zmiany w plikach

### Zmodyfikowane pliki:

1. **`blog/posts/views.py`** - główne zmiany
   - Import `Http404` zamiast `get_object_or_404`
   - Dodanie metody `get_object()` we wszystkich DetailView
   - Dodanie parametru `format=None` do wszystkich metod
   - Aktualizacja docstringów

2. **`blog/posts/urls.py`**
   - Import `format_suffix_patterns`
   - Dodanie obsługi format suffixes

## Testowanie

### Test 1: Format Suffixes

```bash
# Test z suffixem .json
curl http://localhost:8000/api/categories.json

# Test bez suffixu (działa normalnie)
curl http://localhost:8000/api/categories/
```

### Test 2: Obsługa błędów (Http404)

```bash
# Próba pobrania nieistniejącego obiektu
curl http://localhost:8000/api/posts/999/

# Oczekiwany wynik:
# {"detail":"Not found."}
```

### Test 3: Metoda get_object()

```bash
# GET pojedynczego obiektu - używa get_object()
curl http://localhost:8000/api/topics/1.json

# PUT aktualizacji - również używa get_object()
curl -X PUT http://localhost:8000/api/topics/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Nowy tytuł", "content": "Nowa treść", "category": 1}'

# DELETE - również używa get_object()
curl -X DELETE http://localhost:8000/api/topics/1/
```

### Test 4: Automatyczny skrypt

```bash
# Uruchom kompletny test
./test_apiview.sh
```

## Porównanie przed i po

### CategoryDetailView - Przed:

```python
class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        # ...
```

### CategoryDetailView - Po:

```python
class CategoryDetailView(APIView):
    """
    Retrieve, update or delete a category instance.
    """
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        # ...
```

## Korzyści z refaktoryzacji

1. **Zgodność z DRF Best Practices** - kod jest zgodny z oficjalnym tutorialem Django REST Framework

2. **Lepsza separacja logiki** - metoda `get_object()` centralizuje logikę pobierania obiektów

3. **Format Suffixes** - wsparcie dla różnych formatów odpowiedzi (.json, .api)

4. **Łatwiejsze testowanie** - metoda `get_object()` może być łatwo mockowana w testach

5. **Konsystentna obsługa błędów** - `Http404` zapewnia jednolite zachowanie w całym API

6. **Przygotowanie do dalszej refaktoryzacji** - łatwa migracja do mixins lub generic views w przyszłości

## Następne kroki (opcjonalne)

Zgodnie z tutorialem DRF, można dalej refaktoryzować używając:

1. **Mixins** - `ListModelMixin`, `CreateModelMixin`, etc.
2. **Generic Views** - `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`

Przykład z dokumentacji:
```python
from rest_framework import generics

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

## Weryfikacja zmian

✅ Wszystkie endpointy działają poprawnie  
✅ Format suffixes (.json) działają  
✅ Obsługa błędów (Http404) działa poprawnie  
✅ Metoda get_object() jest używana we wszystkich DetailView  
✅ Kod jest zgodny z DRF Tutorial 3  
✅ Testy automatyczne przechodzą pomyślnie  

## Podsumowanie

Implementacja została zaktualizowana zgodnie z przykładami z **Django REST Framework Tutorial 3: Class-based Views**. Wszystkie zmiany zostały przetestowane i działają poprawnie. API zachowuje pełną kompatybilność wsteczną - wszystkie wcześniejsze endpointy działają bez zmian, z dodatkowymi funkcjami format suffixes.
