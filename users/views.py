

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .serializers import UserSignUpSerializer


class UserSignUpAPIView(CreateAPIView):
    serializer_class = UserSignUpSerializer


