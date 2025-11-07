"""
Widoki API dla aplikacji posts.
Implementacja endpointów dla Category, Topic i Post.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from posts.models import Category, Topic, Post
from posts.serializers import (
    CategorySerializer, 
    TopicSerializer, 
    PostSerializer,
    PostListSerializer
)


# ============================================================================
# CATEGORY VIEWS
# ============================================================================

class CategoryListView(APIView):
    """
    GET: Wyświetlanie listy wszystkich kategorii.
    POST: Dodawanie nowej kategorii.
    """
    
    def get(self, request):
        """Pobierz wszystkie kategorie."""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Utwórz nową kategorię."""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """
    GET: Wyświetlanie pojedynczej kategorii.
    PUT: Aktualizacja kategorii.
    DELETE: Usuwanie kategorii.
    """
    
    def get(self, request, pk):
        """Pobierz kategorię o podanym ID."""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Zaktualizuj kategorię."""
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Usuń kategorię."""
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategorySearchView(APIView):
    """
    GET: Wyszukiwanie kategorii po nazwie (zawiera podany łańcuch znaków).
    """
    
    def get(self, request):
        """
        Wyszukaj kategorie zawierające podany łańcuch w nazwie.
        Parametr: ?name=szukany_tekst
        """
        search_query = request.query_params.get('name', '')
        
        if not search_query:
            return Response(
                {'error': 'Parametr "name" jest wymagany.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        categories = Category.objects.filter(name__icontains=search_query)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# ============================================================================
# TOPIC VIEWS
# ============================================================================

class TopicListView(APIView):
    """
    GET: Wyświetlanie listy wszystkich tematów.
    POST: Dodawanie nowego tematu.
    """
    
    def get(self, request):
        """Pobierz wszystkie tematy."""
        topics = Topic.objects.select_related('category').all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Utwórz nowy temat."""
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    """
    GET: Wyświetlanie pojedynczego tematu.
    PUT: Aktualizacja tematu.
    DELETE: Usuwanie tematu.
    """
    
    def get(self, request, pk):
        """Pobierz temat o podanym ID."""
        topic = get_object_or_404(Topic.objects.select_related('category'), pk=pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Zaktualizuj temat."""
        topic = get_object_or_404(Topic, pk=pk)
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Usuń temat."""
        topic = get_object_or_404(Topic, pk=pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopicSearchView(APIView):
    """
    GET: Wyszukiwanie tematów po tytule (zawiera podany łańcuch znaków).
    """
    
    def get(self, request):
        """
        Wyszukaj tematy zawierające podany łańcuch w tytule.
        Parametr: ?name=szukany_tekst (lub ?title=szukany_tekst)
        """
        # Obsługa obu parametrów dla spójności
        search_query = request.query_params.get('name') or request.query_params.get('title', '')
        
        if not search_query:
            return Response(
                {'error': 'Parametr "name" lub "title" jest wymagany.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        topics = Topic.objects.filter(title__icontains=search_query).select_related('category')
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


# ============================================================================
# POST VIEWS
# ============================================================================

class PostListView(APIView):
    """
    GET: Wyświetlanie listy wszystkich postów.
    POST: Dodawanie nowego posta.
    """
    
    def get(self, request):
        """Pobierz wszystkie posty."""
        posts = Post.objects.select_related('topic', 'topic__category', 'created_by').all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Utwórz nowy post."""
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    GET: Wyświetlanie pojedynczego posta.
    PUT: Aktualizacja posta.
    DELETE: Usuwanie posta.
    """
    
    def get(self, request, pk):
        """Pobierz post o podanym ID."""
        post = get_object_or_404(
            Post.objects.select_related('topic', 'topic__category', 'created_by'), 
            pk=pk
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Zaktualizuj post."""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """Usuń post."""
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostSearchView(APIView):
    """
    GET: Wyszukiwanie postów po tytule (zawiera podany łańcuch znaków).
    """
    
    def get(self, request):
        """
        Wyszukaj posty zawierające podany łańcuch w tytule.
        Parametr: ?name=szukany_tekst (lub ?title=szukany_tekst)
        """
        # Obsługa obu parametrów dla spójności
        search_query = request.query_params.get('name') or request.query_params.get('title', '')
        
        if not search_query:
            return Response(
                {'error': 'Parametr "name" lub "title" jest wymagany.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        posts = Post.objects.filter(
            title__icontains=search_query
        ).select_related('topic', 'topic__category', 'created_by')
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
