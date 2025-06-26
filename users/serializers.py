
from .models import User, Profile
from django.contrib.auth import password_validation

from rest_framework import  serializers


# password validation
def validate_password(password):
    password_validation.validate_password(password)
    return password


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['avatar', 'address', 'interests','skills']












