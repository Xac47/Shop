from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at'])
        ]


class Social_links(models.Model):
    instagram = models.URLField()
    telegram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()

    class Meta:
        abstract = True
