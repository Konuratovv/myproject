from rest_framework import serializers
from apps.users.models import CustomUser

from apps.users.serializers import ProfileSerializer
from apps.webapp.models import Comment, Post, Tag

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email']

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag 
        fields = ['title']

class CommentSerializer(serializers.ModelSerializer):
    comment_author = AuthorSerializer()

    class Meta:
        model = Comment 
        fields = [
            'comment_author',
            'text',
        ]

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'description',
            'date',
            'tags',
        ]

class DetailPostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()   
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_viewed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'description',
            'tags',
            'date',
            'comments',
            'likes_count',
            'is_liked',
            'is_viewed',
        ]                      

    def get_comments(self, post):
        return CommentSerializer(instance=post.comments, many=True).data   
    
    def get_is_liked(self, post):
        return self.context.get('request').user in post.likes
    
    def get_is_viewed(self, post):
        return self.context.get('request').user in post.views