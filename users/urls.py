from django.urls import path
from .views import (
    UserSignUpAPIView,
    UserProfileUpdateAPIView,
)

from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/',UserSignUpAPIView.as_view(), name='signup-api'),
    path('login/',TokenObtainPairView.as_view(), name='login'),

    path('profile/update/',UserProfileUpdateAPIView.as_view(), name='profile-update-api'),

]