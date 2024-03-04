from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.core.exceptions import ObjectDoesNotExist
from apps.users.models import Profile, FollowUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from apps.users.serializers import EmailVerificationSerializer, FollowUserSerializer, LoginSerializer, ProfileSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.utils import send_verification_email


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

            send_verification_email(user.email)

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
        
        if not user.is_verified:
            send_verification_email(user.email)
            return Response({'status': 'This user is not valid!'})
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
    
class EmailVerificationAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        user = Profile.objects.filter(email=self.request.data['email']).first()
        verify_code = self.request.data.get('code')
        if user.code == verify_code:
            user.is_verified = True
            user.code = None
            user.save()
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            return Response({'access_token': str(access_token), 'refresh_token': str(refresh_token)})
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

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
    
class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user.id
        profile = Profile.objects.get(id=user)
        return profile

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data)
    
class FollowUserAPIView(generics.CreateAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = Profile.objects.get(id=self.request.user.id)
        try:
            follow = Profile.objects.get(id=self.request.data.get('following'))
        except ObjectDoesNotExist:
            return Response({'status': 'user not found!'})
        
        try:
            FollowUser.objects.get(following=user,
                                   follower=follow)
            return Response({'status': f'You already followed'})
        except ObjectDoesNotExist:
            follow_user = FollowUser.objects.create(following=user,
                                    follower=follow)
            user.followers_count += 1
            user.save()
            follow_user.save()
        return Response({'status': f'success{user.followers_count}'})
    
class UnfollowUserAPIView(generics.DestroyAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = Profile.objects.get(id=self.request.user.id)
        try:
            follow = Profile.objects.get(id=self.request.data.get('following'))
        except ObjectDoesNotExist:
            return Response({'status': 'user not found!'})
        try:
            unfollow_user = FollowUser.objects.get(following=user,
                                   follower=follow)
            unfollow_user.delete()
            user.followers_count -= 1
            user.save()
            return Response({'status': f'success{user.followers_count}'})
        except ObjectDoesNotExist:
            return Response({'status': 'user is not followed'})
