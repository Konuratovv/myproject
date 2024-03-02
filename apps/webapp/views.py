from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.webapp.models import Post
from apps.webapp.serializers import DetailPostSerializer, PostSerializer
# Create your views here.

@api_view(['GET'])
def posts_api_view(request):
    posts = Post.objects.prefetch_related('tags').select_related('author').all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_detail_api_view(request, pk):
    post = Post.objects.get(id=pk)
    serializer = DetailPostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)

