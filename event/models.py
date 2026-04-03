from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.utils import timezone

from django_resized import ResizedImageField
from PIL import Image

User = get_user_model()

def upload_location(instance, filename, *args, **kwargs):
    file_path = f'event_pictures/{instance.title}/{filename}'
    return file_path

class Event(models.Model):
    POST_STATUS = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    venue = models.CharField(max_length=255)
    fee = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    post_status = models.CharField(max_length=15, choices=POST_STATUS, default='Published')
    picture = ResizedImageField(size=[680, 370], upload_to=upload_location, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_published',)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        if self.is_published and self.date_published is None:
            self.date_published = timezone.now()

        super(Event, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("event:event_detail", kwargs={
            "slug": slugify(self.slug),
        })

    @property
    def get_image_url(self):
        return self.picture.url