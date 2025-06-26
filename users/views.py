from rest_framework import  generics
from .serializers import (
    UserSignUpSerializer,
    UserProfileSerializer,
)
from rest_framework import views
from rest_framework.response import  Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import  ValidationError
from .models import Profile


"Signup API"
class UserSignUpAPIView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer


" Update API, only authenticate users can update profile"
class UserProfileUpdateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def put(self,request):
        profile = self.get_object()
        serializer = UserProfileSerializer(instance=profile,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)








































