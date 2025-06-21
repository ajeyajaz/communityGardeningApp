from django.urls import path

from .views import UserSignUpAPIView



urlpatterns = [
    path('signup/',UserSignUpAPIView.as_view(), name='signup-api'),

]