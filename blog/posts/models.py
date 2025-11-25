from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Model kategorii dla postów."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    """Model tematu powiązanego z kategorią."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='topics'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ['title']
    
    def __str__(self):
        return self.title


class Post(models.Model):
    """Model posta na blogu."""
    title = models.CharField(max_length=150)
    text = models.TextField()
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=True
    )
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
        permissions = [
            ("can_edit_others_posts", "Can edit posts of other users"),
        ]
    
    def __str__(self):
        # Pierwsze 5 wyrazów tekstu posta + '...' jeżeli dłuższy
        words = self.text.split()
        if len(words) > 5:
            return ' '.join(words[:5]) + '...'
        return ' '.join(words)
