from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from apps.users.models import Profile
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from apps.users.serializers import LoginSerializer, ProfileSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = Profile.objects.create_user(
                email = serializer.validated_data['email'],
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                password = serializer.validated_data['password']
            )

            return Response({'status': 'success'})
        return Response({'status':'error'})
    
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):
        user = Profile.objects.filter(email=self.request.data['email']).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(self.request.data['password']):
            raise AuthenticationFailed('Incorrect password')
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
    
class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user.id
        profile = Profile.objects.get(id=user)
        return profile
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)