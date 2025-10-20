from django.contrib import admin
from .models import Category, Topic, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    list_display = ['name', 'created_at']
    list_filter = ['name']
    search_fields = ['name', 'description']
    ordering = ['name']
    fields = ['name', 'description']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin interface for Topic model."""
    list_display = ['title', 'category', 'created_at', 'updated_at']
    list_filter = ['category', 'title', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""
    list_display = ['title', 'topic_with_category', 'created_by', 'text_preview', 'created_at', 'updated_at']
    readonly_fields = ['created_at']
    list_filter = ['topic', 'topic__category', 'created_by', 'created_at']
    search_fields = ['title', 'text']
    ordering = ['-created_at']
    prepopulated_fields = {'slug': ('title',)}
    
    @admin.display(description='Topic (Kategoria)')
    def topic_with_category(self, obj):
        """Wyświetla topic w formacie 'nazwa topiku (nazwa kategorii)'."""
        return f"{obj.topic.title} ({obj.topic.category.name})"
    
    def text_preview(self, obj):
        """Wyświetla pierwsze 5 wyrazów tekstu posta + '...' jeżeli dłuższy."""
        words = obj.text.split()
        if len(words) > 5:
            return ' '.join(words[:5]) + '...'
        return ' '.join(words)
    text_preview.short_description = 'Podgląd tekstu'
    date_hierarchy = 'created_at'
