import uuid
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.utils import timezone

from django_resized import ResizedImageField
from PIL import Image

User = get_user_model()

def generate_post_code():
    return str(uuid.uuid4())[:10]

def upload_location(instance, filename, *args, **kwargs):
    file_path = f'article_pictures/{instance.title}/{filename}'
    return file_path

class Article(models.Model):
    POST_STATUS = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.CharField(max_length=10, default=generate_post_code, unique=True) 
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    field = models.CharField(max_length=25, blank=True, null=True)
    body = models.TextField()
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

        super(Article, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("article:article_detail", kwargs={
            "slug": slugify(self.slug),
        })

    @property
    def get_image_url(self):
        return self.picture.url