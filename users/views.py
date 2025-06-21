from rest_framework.generics import(
    CreateAPIView,
    UpdateAPIView,
    ListAPIView
)
from .serializers import (
    UserSignUpSerializer,
    UserProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from .permissions import IsOwner

from .models import Profile,User


class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSignUpSerializer


class UserProfileCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        if Profile.objects.filter(user=self.request.user).exists():
            raise ValidationError({'detail': 'profile already exists'})
        user = self.request.user
        serializer.save(user=user)


class UserProfileUpdateAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = UserProfileSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer


























