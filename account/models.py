from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from base.models import ImageBaseModel
from .managers import UserManager


# from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin, ImageBaseModel):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    image = models.ImageField('Фото', upload_to='user_images/%Y/%m/%d/', blank=True, null=True)
    # phone_number = PhoneNumberField(region='RU', verbose_name='Phone')
    email = models.EmailField(_('email address'), unique=True)
    email_verify = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
