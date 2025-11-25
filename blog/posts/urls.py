"""
URL configuration dla aplikacji posts.
Zgodne z Django REST Framework Tutorial 3 - Class-based Views.
Lab 6 - Autentykacja i uprawnienia.
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

app_name = 'posts'

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/search/', views.CategorySearchView.as_view(), name='category-search'),
    
    # Topic endpoints
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    path('topics/search/', views.TopicSearchView.as_view(), name='topic-search'),
    
    # Post endpoints
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/search/', views.PostSearchView.as_view(), name='post-search'),
    
    # ========================================================================
    # LAB 6 - Authenticated endpoints
    # ========================================================================
    
    # Zadanie 2: Posty aktualnie zalogowanego użytkownika
    path('users/posts/', views.user_posts_list, name='user-posts'),
    
    # Zadanie 4: Osobne endpointy dla PUT i DELETE z różnymi metodami autentykacji
    path('posts/update/<int:pk>/', views.post_update, name='post-update'),
    path('posts/delete/<int:pk>/', views.post_delete, name='post-delete'),
    
    # Zadanie 5: Tematy dla danej kategorii (tylko token auth)
    path('categories/<int:category_id>/topics/', views.category_topics_list, name='category-topics'),

    # ========================================================================
    # LAB 7 - Permissions
    # ========================================================================
    
    # Zadanie 2: Widok z ręcznym sprawdzaniem uprawnień
    path('categories/<int:pk>/simple/', views.category_view, name='category-simple'),
    
    # Zadanie 3: Widok z custom permission
    path('posts/<int:pk>/moderator/', views.PostDetailModeratorView.as_view(), name='post-moderator'),

    # Zadanie 4: Widok z CustomDjangoModelPermissions
    path('categories/<int:pk>/permissions/', views.CategoryDetailPermissionView.as_view(), name='category-permissions'),
]

# Dodanie obsługi format suffixes (.json, .api, etc.)
urlpatterns = format_suffix_patterns(urlpatterns)
