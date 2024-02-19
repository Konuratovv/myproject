from rest_framework import generics
from apps.webapp.models import Post
from rest_framework.permissions import IsAuthenticated
from apps.webapp.serializers import DetailPostSerializer, PostSerializer
# Create your views here.

class PostAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author').all()
    permission_classes = [IsAuthenticated]

class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = DetailPostSerializer
    queryset = Post.objects.select_related('author').all()
    permission_classes = [IsAuthenticated]