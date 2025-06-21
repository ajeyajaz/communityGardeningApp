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
        return f'{self.username} - {self.email}'











