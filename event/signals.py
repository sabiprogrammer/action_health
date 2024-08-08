from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Event

@receiver(post_delete, sender=Event)
def delete_event_picture(sender, instance, *args, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)
