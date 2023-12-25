from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, UserActivity

@receiver(post_save, sender=Profile)
def create_target_model(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(user=instance)