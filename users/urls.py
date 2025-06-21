from django.urls import path
from .views import (
    UserSignUpAPIView,
    UserProfileCreateAPIView,
    UserProfileUpdateAPIView,
    UserList,
)

from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [
    path('signup/',UserSignUpAPIView.as_view(), name='signup-api'),
    path('login/',TokenObtainPairView.as_view(), name='login'),

    path('profile/',UserProfileCreateAPIView.as_view(), name='profile-create-api'),
    path('profile/<int:pk>/',UserProfileUpdateAPIView.as_view(), name='profile-update-api'),

    path('list/',UserList.as_view())

]