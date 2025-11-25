"""
Widoki API dla aplikacji posts.
Implementacja endpointów dla Category, Topic i Post.
Bazowane na przykładach z Django REST Framework Tutorial 3.
Lab 6 - Autentykacja i uprawnienia.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from posts.models import Category, Topic, Post
from posts.permissions import CustomDjangoModelPermissions, CanEditOthersPosts
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
    List all categories, or create a new category.
    """
    
    def get(self, request, format=None):
        """Pobierz wszystkie kategorie."""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Utwórz nową kategorię."""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """
    Retrieve, update or delete a category instance.
    """
    
    def get_object(self, pk):
        """
        Pobierz kategorię o podanym ID lub zwróć Http404.
        """
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """Pobierz kategorię."""
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Zaktualizuj kategorię."""
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Usuń kategorię."""
        category = self.get_object(pk)
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
    List all topics, or create a new topic.
    """
    
    def get(self, request, format=None):
        """Pobierz wszystkie tematy."""
        topics = Topic.objects.select_related('category').all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Utwórz nowy temat."""
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    """
    Retrieve, update or delete a topic instance.
    """
    
    def get_object(self, pk):
        """
        Pobierz temat o podanym ID lub zwróć Http404.
        """
        try:
            return Topic.objects.select_related('category').get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """Pobierz temat."""
        topic = self.get_object(pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Zaktualizuj temat."""
        topic = self.get_object(pk)
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """Usuń temat."""
        topic = self.get_object(pk)
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
    List all posts, or create a new post.
    """
    
    def get(self, request, format=None):
        """Pobierz wszystkie posty."""
        posts = Post.objects.select_related('topic', 'topic__category', 'created_by').all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Utwórz nowy post."""
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# ============================================================================
# AUTHENTICATED USER VIEWS (LAB 6 - ZADANIE 2)
# ============================================================================

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_posts_list(request):
    """
    Zwraca listę postów utworzonych przez aktualnie zalogowanego użytkownika.
    Wymaga uwierzytelnienia (IsAuthenticated).
    
    Endpoint: /api/users/posts/
    """
    # Filtruj posty po aktualnie zalogowanym użytkowniku
    posts = Post.objects.filter(
        created_by=request.user
    ).select_related('topic', 'topic__category', 'created_by')
    
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)


# ============================================================================
# POST OPERATIONS WITH DIFFERENT AUTHENTICATION (LAB 6 - ZADANIE 4)
# ============================================================================

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    """
    Aktualizacja posta (PUT).
    Wymaga uwierzytelnienia przez sesję lub Basic Auth.
    
    Endpoint: /api/posts/update/<pk>/
    """
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


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    """
    Usunięcie posta (DELETE).
    Wymaga uwierzytelnienia przez TOKEN.
    
    Endpoint: /api/posts/delete/<pk>/
    Header: Authorization: Token <token_value>
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================================
# CATEGORY TOPICS VIEW (LAB 6 - ZADANIE 5)
# ============================================================================

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_topics_list(request, category_id):
    """
    Zwraca listę wszystkich tematów (Topic) dla podanej kategorii.
    Dostęp tylko do odczytu, wymaga uwierzytelnienia przez TOKEN.
    
    Endpoint: /api/categories/<category_id>/topics/
    Header: Authorization: Token <token_value>
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404
    
    # Pobierz wszystkie tematy dla danej kategorii
    topics = Topic.objects.filter(category=category).select_related('category')
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

# ============================================================================
# LAB 7 VIEWS
# ============================================================================

# Zadanie 2
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def category_view(request, pk):
    if not request.user.has_perm('posts.view_category'):
        raise PermissionDenied()
    try:
        category = Category.objects.get(pk=pk)
        return HttpResponse(f"Kategoria: {category.name}")
    except Category.DoesNotExist:
        return HttpResponse(f"Kategoria o id={pk} nie istnieje.")

# Zadanie 4
class CategoryDetailPermissionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = Category.objects.all() # Required for DjangoModelPermissions

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
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Zadanie 3
class PostDetailModeratorView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, CanEditOthersPosts]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
