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
        ]

class DetailPostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()   

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'description',
            'tags',
            'date',
            'comments',
        ]                      

    def get_comments(self, post):
        return CommentSerializer(instance=post.comments, many=True).data   