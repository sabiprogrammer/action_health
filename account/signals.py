from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        # Profile.objects.create(user=instance)
        print("PROFILE CREATED")
    print('CREATED', created)
    print('SENDER', sender)
    # print('SENDER - dir', dir(sender))

def update_profile(sender, instance, created, *args, **kwargs):
    if created:
        # instance.profile.save()
        print("PROFILE UPDATED")
        print('CREATED', created)
        print('SENDER', sender)

# post_save.connect(update_profile, sender=User)