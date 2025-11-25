# Lab 7 - Uprawnienia w Django i DRF - Podsumowanie

## Zrealizowane zadania

### ✅ Zadanie 1: Grupy i uprawnienia w panelu admina

**Implementacja:**
- Utworzono grupę `Lab7_Group`.
- Przypisano do niej uprawnienie `posts.view_category`.
- Utworzono użytkownika `lab7user` (staff) i przypisano do grupy.

**Skrypt setup:** `setup_lab7.py`

### ✅ Zadanie 2: Widok z ręcznym sprawdzaniem uprawnień

**Endpoint:** `GET /api/categories/<pk>/simple/`

**Implementacja:**
```python
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def category_view(request, pk):
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied()
    # ...
```

**Test:**
- `lab7user` (ma uprawnienie) -> 200 OK
- `testuser` (brak uprawnienia) -> 403 Forbidden

### ✅ Zadanie 3: Własne uprawnienie `can_edit_others_posts`

**Implementacja:**

1. **Model `Post`:**
```python
class Meta:
    permissions = [
        ("can_edit_others_posts", "Can edit posts of other users"),
    ]
```

2. **Permission Class (`posts/permissions.py`):**
```python
class CanEditOthersPosts(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        return request.user.has_perm('posts.can_edit_others_posts')
```

3. **Widok (`PostDetailModeratorView`):**
```python
permission_classes = [IsAuthenticated, CanEditOthersPosts]
```

**Test:**
- `moderator` (ma uprawnienie) -> 200 OK (edycja cudzego posta)
- `lab7user` (brak uprawnienia) -> 403 Forbidden

### ✅ Zadanie 4: `CustomDjangoModelPermissions`

**Implementacja:**

1. **Klasa (`posts/permissions.py`):**
```python
class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
```

2. **Widok (`CategoryDetailPermissionView`):**
```python
permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
queryset = Category.objects.all()
```

**Test:**
- `lab7user` (ma `view_category`) -> GET: 200 OK
- `lab7user` (brak `change_category`) -> PUT: 403 Forbidden
- `testuser` (brak `view_category`) -> GET: 403 Forbidden

---

## Pliki

- `blog/posts/models.py` - dodano permissions w Meta
- `blog/posts/permissions.py` - nowe klasy uprawnień
- `blog/posts/views.py` - nowe widoki
- `blog/posts/urls.py` - nowe endpointy
- `blog/setup_lab7.py` - skrypt tworzący dane testowe
- `test_lab7.sh` - skrypt testujący

## Uruchomienie testów

```bash
./test_lab7.sh
```
