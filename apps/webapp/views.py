from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .services import CRUDAPIView
from apps.webapp.models import Post
from apps.webapp.serializers import DetailPostSerializer
# Create your views here.

class PostAPIView(CRUDAPIView):
    serializer_class = DetailPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

class PostLikeAPIView(generics.UpdateAPIView):
    serializer_class = DetailPostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        try:
            post_id = self.request.data.get('post_id')
            post = Post.objects.get(pk=post_id)
            serializer = self.get_serializer(post)
            is_liked = serializer.data['is_liked']
            if is_liked == False:
                post.likes.add(user)
                post.save()
                serializer.data['is_liked'] = True
                post.likes_count += 1
                return Response(status={'status': 'You liked successfully!'})
            else:
                post.likes.remove(user)
                post.save()
                serializer.data['is_liked'] = False
                post.likes_count -= 1
                return Response(status={'status': 'You removed like successfully!'})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LikedPostsAPIView(generics.ListAPIView):
    serializer_class = DetailPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request, *args, **kwargs):
        user = self.request.user
        liked_posts = Post.objects.filter(likes=user)
        return liked_posts
