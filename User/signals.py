from django.dispatch import receiver
from .models import Profile, CustomUser
from django.db.models.signals import post_save
from Task.models import Board


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=CustomUser)
def create_board(sender, instance, created, **kwargs):
    if created:
        Board.objects.create(title="Main board", description="Main board for your tasks", user=instance)


