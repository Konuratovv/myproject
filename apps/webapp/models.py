from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import CustomUser

# Create your models here.

class Tag(models.Model):
    title = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f"{self.title}"

class Post(models.Model):
    title = models.CharField(max_length=150)
    post_image = models.ImageField(upload_to='posts', verbose_name='Картинка')
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='post')
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post')
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    likes_count = models.PositiveIntegerField(default=0, blank=True)
    views = models.ManyToManyField(CustomUser, related_name='post_views', blank=True)
    views_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Comment(models.Model):
    comment_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    
    
    
    
    