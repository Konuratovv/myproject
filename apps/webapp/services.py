from rest_framework.mixins import UpdateModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthorOrReadOnly

class CRUDAPIView(UpdateModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    def update(self, request, *args, **kwargs):
        isntance = self.get_object()
        serializer = self.get_serializer(isntance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instanse = self.get_object()
            instanse.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == "PUT" or self.request.method == "DELETE":
            return [IsAuthorOrReadOnly]
        return super().get_permissions()
