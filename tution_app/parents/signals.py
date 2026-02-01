from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ParentProfile

@receiver(post_save, sender=ParentProfile)
def approve_parent(sender, instance, **kwargs):
    if instance.is_approved and not instance.user.is_active:
        instance.user.is_active = True
        instance.user.save()
