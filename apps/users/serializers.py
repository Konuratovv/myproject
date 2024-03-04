from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from apps.users.models import CustomUser, FollowUser, Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Profile.objects.all())])

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password'
        ]

    def validate(self, data):
        if data['confirm_password'] != data['password']:
            data = []
            raise serializers.ValidationError('Passwords did not match!')
        return data 
    
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'email',
            'password',
        ]
    
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'desription',
            'city',
            'email',
        ]

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'code',
            'email',
        ]

class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = '__all__'