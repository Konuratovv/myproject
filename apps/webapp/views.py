from rest_framework.permissions import IsAuthenticated
from .services import CRUDAPIView
from apps.webapp.models import Post
from apps.webapp.serializers import DetailPostSerializer
# Create your views here.

class PostAPIView(CRUDAPIView):
    serializer_class = DetailPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

