from django.db import models

from base.models import BaseModel


class SubscribeEmail(BaseModel):
    email = models.EmailField(unique=True, max_length=255)

    class Meta:
        verbose_name = 'Подписка на рассылку'
        verbose_name_plural = 'Подписки на рассылку'


    def __str__(self):
        return self.email
