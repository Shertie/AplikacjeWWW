"""
URL configuration dla aplikacji posts.
Zgodne z Django REST Framework Tutorial 3 - Class-based Views.
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
]

# Dodanie obsługi format suffixes (.json, .api, etc.)
urlpatterns = format_suffix_patterns(urlpatterns)
