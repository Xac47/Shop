from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from coupons.managers import ActiveManager


class Coupon(models.Model):
    code = models.CharField('Купон', max_length=50, unique=True)
    valid_from = models.DateField('Начало действия')
    valid_to = models.DateField('Конец действия')
    discount = models.IntegerField('Скидка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField('Статус', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ('-is_active',)
        indexes = [
            models.Index(fields=['-updated_at'])
        ]
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return f'{self.code}, {self.discount}'
