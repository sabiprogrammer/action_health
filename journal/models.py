from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.utils import timezone

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
    # is_edited = models.BooleanField(default=False)
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

        super(Journal, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("journal:journal_detail", kwargs={
            "slug": slugify(self.slug),
        })
