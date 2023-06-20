from django.db import models
from django.utils.safestring import mark_safe


class ImageBaseModel(models.Model):
    image = None

    def get_image(self, width=50, height=50):
        return mark_safe(f'<img src={self.image.url} width="{width}" height="{height}">')

    class Meta:
        abstract = True


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
