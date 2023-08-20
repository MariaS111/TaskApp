from django.db import models
from django.contrib.auth.models import AbstractUser
from TaskApp import settings


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    profile_image = models.ImageField(upload_to='users_profile_images/', blank=True, default='base.png')

    def __str__(self):
        return f'{self.user.username} Profile'