from django.db import models


class ImageBaseModel(models.Model):
    image = None
    image_svg = None

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        if self.image_svg and hasattr(self.image_svg, 'url'):
            return self.image_svg.url
        else:
            return 'static/assets/imgs/net-foto.jpg'

    class Meta:
        abstract = True


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Social_links(models.Model):
    instagram = models.URLField()
    telegram = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()

    class Meta:
        abstract = True
