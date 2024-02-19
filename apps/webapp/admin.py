from django.contrib import admin

from apps.webapp.models import Post, Comment, Tag

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = [
        'id',
        'title',
    ]

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = [
        'id',
        'title',
        'description',
        'date',
        'author',
    ]