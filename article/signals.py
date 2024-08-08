# from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

from .models import Article

@receiver(post_delete, sender=Article)
def delete_article_picture(sender, instance, *args, **kwargs):
    if instance.picture:
        instance.picture.delete(save=False)

'''
@receiver(post_save, sender=Article)
def resize_article_picture(sender, instance, *args, **kwargs):
    if instance.picture:
        img = Image.open(instance.picture.path)
        if img.height > 500 or img.width > 900:
            output = (400, 500)
            img.thumbnail(output)
            img.save(instance.picture.path)
'''
