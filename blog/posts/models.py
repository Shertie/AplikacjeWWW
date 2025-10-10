from django.db import models


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
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
