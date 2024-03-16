from .services import CRUDAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.webapp.models import Post
from apps.webapp.serializers import DetailPostSerializer, PostSerializer
from .tasks import simple_task
# Create your views here.

class PostAPIView(CRUDAPIView):
    serializer_class = PostSerializer
    queryset = Post

