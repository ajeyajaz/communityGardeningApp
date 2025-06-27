from django.db import models
from  django.contrib.auth.models import AbstractUser

#Custom user model
class User(AbstractUser):
    email = models.EmailField(unique=True,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.username}'

#user Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True,null=True)
    address = models.CharField(max_length=255,blank=True)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"








