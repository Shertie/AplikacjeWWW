"""
Serializatory dla aplikacji posts.
"""
from rest_framework import serializers
from posts.models import Category, Topic, Post
from django.contrib.auth.models import User
from django.utils import timezone
import re


class CategorySerializer(serializers.Serializer):
    """
    Serializator dla modelu Category dziedziczący po serializers.Serializer.
    Implementuje wszystkie pola i metody create/update ręcznie.
    
    Nadpisane metody:
    - validate_name: Zamienia nazwę na format Title Case
    - create: Tworzy nową kategorię
    - update: Aktualizuje istniejącą kategorię
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    created_at = serializers.DateTimeField(read_only=True)
    
    def validate_name(self, value):
        """
        Walidacja nazwy kategorii.
        Zamienia pierwszą literę każdego słowa na wielką (Title Case).
        Usuwa nadmiarowe białe znaki.
        """
        # Usuń nadmiarowe białe znaki
        cleaned_name = ' '.join(value.split())
        # Zamień na Title Case
        return cleaned_name.title()
    
    def validate(self, data):
        """
        Walidacja na poziomie obiektu.
        Sprawdza unikalność nazwy kategorii (tylko podczas tworzenia).
        """
        # Podczas tworzenia nowej kategorii (brak instance)
        if not self.instance:
            name = data.get('name')
            if Category.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError({
                    'name': 'Kategoria o tej nazwie już istnieje.'
                })
        return data
    
    def create(self, validated_data):
        """
        Tworzenie nowej instancji Category.
        """
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Aktualizacja istniejącej instancji Category.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu User (wbudowany model Django).
    Używa ModelSerializer dla uproszczenia.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        """
        Zwraca pełne imię i nazwisko użytkownika.
        """
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username


class TopicSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Topic.
    Zawiera zagnieżdżone informacje o kategorii.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Topic
        fields = [
            'id', 'title', 'content', 'category', 'category_name', 
            'category_detail', 'posts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_posts_count(self, obj):
        """
        Zwraca liczbę postów przypisanych do tego tematu.
        """
        return obj.posts.count()
    
    def validate_title(self, value):
        """
        Walidacja tytułu.
        Usuwa nadmiarowe białe znaki i kapitalizuje pierwszą literę.
        """
        cleaned_title = ' '.join(value.split())
        return cleaned_title.capitalize()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializator dla modelu Post.
    Zawiera zagnieżdżone informacje o topic, category i autorze.
    
    Walidacje:
    - title: może zawierać tylko litery (i spacje)
    - created_at: nie może być z przyszłości
    
    Nadpisane metody:
    - create: Automatycznie przypisuje zalogowanego użytkownika jako autora
    - validate_title: Sprawdza czy zawiera tylko litery
    - validate_created_at: Sprawdza czy data nie jest z przyszłości
    - validate_text: Usuwa nadmiarowe białe znaki z tekstu
    """
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    category_name = serializers.CharField(source='topic.category.name', read_only=True)
    author_username = serializers.CharField(source='created_by.username', read_only=True)
    author_detail = UserSerializer(source='created_by', read_only=True)
    word_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'text', 'slug', 'topic', 'topic_title', 
            'category_name', 'created_by', 'author_username', 'author_detail',
            'word_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'updated_at']
        # created_at nie jest w read_only_fields, aby umożliwić walidację daty
    
    def get_word_count(self, obj):
        """
        Zwraca liczbę słów w tekście posta.
        """
        return len(obj.text.split())
    
    def validate_title(self, value):
        """
        Walidacja tytułu - może zawierać tylko litery (i spacje).
        Usuwa nadmiarowe białe znaki.
        """
        # Usuń nadmiarowe białe znaki
        cleaned_value = ' '.join(value.split())
        
        # Sprawdź czy zawiera tylko litery i spacje (obsługa polskich znaków)
        if not re.match(r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ\s]+$', cleaned_value):
            raise serializers.ValidationError(
                'Tytuł może zawierać tylko litery i spacje (bez cyfr i znaków specjalnych).'
            )
        
        return cleaned_value
    
    def validate_created_at(self, value):
        """
        Walidacja daty utworzenia - nie może być z przyszłości.
        """
        if value and value > timezone.now():
            raise serializers.ValidationError(
                'Data utworzenia nie może być z przyszłości.'
            )
        return value
    
    def validate_text(self, value):
        """
        Walidacja tekstu.
        Usuwa nadmiarowe białe znaki i formatuje tekst.
        """
        # Usuń nadmiarowe białe znaki
        lines = value.split('\n')
        cleaned_lines = [' '.join(line.split()) for line in lines]
        return '\n'.join(cleaned_lines)
    
    def create(self, validated_data):
        """
        Tworzenie nowego posta.
        Automatycznie przypisuje zalogowanego użytkownika jako autora,
        jeśli nie został podany explicitly.
        Jeśli created_at nie został podany, używa aktualnej daty.
        """
        # Jeśli created_by nie został podany, użyj użytkownika z kontekstu
        if 'created_by' not in validated_data:
            request = self.context.get('request')
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                validated_data['created_by'] = request.user
        
        # Jeśli created_at nie został podany, Django automatycznie ustawi aktualną datę
        return Post.objects.create(**validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Uproszczony serializator dla listy postów.
    Zawiera tylko podstawowe informacje bez zagnieżdżonych danych.
    """
    topic_title = serializers.CharField(source='topic.title', read_only=True)
    author_username = serializers.CharField(source='created_by.username', read_only=True)
    preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'preview', 'slug', 'topic_title', 
            'author_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_preview(self, obj):
        """
        Zwraca pierwsze 5 wyrazów tekstu jako podgląd.
        """
        words = obj.text.split()
        if len(words) > 5:
            return ' '.join(words[:5]) + '...'
        return ' '.join(words)
