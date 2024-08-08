from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

User = get_user_model()

class Journal(models.Model):
    POST_STATUS = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.TextField()
    keywords = models.CharField(max_length=255, blank=True, null=True)
    full_journal = models.TextField()
    type = models.CharField(max_length=25, blank=True, null=True)
    field = models.CharField(max_length=25)
    post_status = models.CharField(max_length=15, choices=POST_STATUS, default='Published')
    reviewed_by = models.CharField(max_length=255, blank=True, null=True)
    link_to_profile = models.CharField(max_length=255, blank=True, null=True)
    contributor_id_number = models.CharField(max_length=255, blank=True, null=True)
    special_note = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_published',)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Journal, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("journal:journal_detail", kwargs={
            "slug": slugify(self.slug),
        })

    @property
    def get_image_url(self):
        return self.picture.url
