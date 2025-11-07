"""
URL configuration dla aplikacji posts.
"""
from django.urls import path
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
