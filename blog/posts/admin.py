from django.contrib import admin
from .models import Category, Topic


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    fields = ['name', 'description']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin interface for Topic model."""
    list_display = ['title', 'category', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
