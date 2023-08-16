from django.dispatch import receiver
from .models import Profile, CustomUser
from django.db.models.signals import post_save
from Task.models import Board
from django.contrib.auth import get_user_model


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_save, sender=CustomUser)
# def create_main_board(sender, instance, **kwargs):
#     Board.objects.create(title='Main board')

