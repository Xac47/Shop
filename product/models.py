from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from base.models import BaseModel, ImageBaseModel
from autoslug import AutoSlugField

from product.managers import ManagerCustom

User = get_user_model()


class Category(BaseModel):
    name = models.CharField('Имя', max_length=200, unique=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField('Name', max_length=100, unique=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Product(BaseModel, ImageBaseModel):
    class Status(models.TextChoices):
        PUBLISHED = ('PB', 'Published')
        DRAFT = ('DF', 'Draft')

    title = models.CharField('Заголовок', max_length=250)
    # slug = AutoSlugField(always_update=True, populate_from='title', max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    image = models.ImageField('Изображение', upload_to='product_images/%Y/%m/%d/%H/')
    desc = models.TextField('Описание')
    specifications = models.TextField('Характеристики')
    status = models.CharField('Статус', choices=Status.choices, default=Status.DRAFT, max_length=2)

    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField('Скидка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    # Managers

    objects = models.Manager()
    published = ManagerCustom('Published')

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at', 'title', 'status'])
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_discount_price(self):
        if not self.discount:
            return self.price
        price = Decimal('self.price') * (Decimal('100') - self.discount) / Decimal('100')
        return price

    def get_reviews(self):
        return self.reviews.filter(parent__isnull = True)


    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')
    image = models.ImageField('Фото', upload_to='product_images/%Y/%m/%d/%H/')
    phote_number = models.SmallIntegerField('Номер фото')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотки'

    def __str__(self):
        return self.phote_number


class Rating(BaseModel):
    STAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6)
    )

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    star = models.PositiveIntegerField(choices=STAR)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name="ratings")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f'{self.star}, {self.product}'


class Reviews(BaseModel):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    message = models.TextField("Сообщение", max_length=500)
    parent = models.ForeignKey('self', verbose_name="Родитель", related_name='children', on_delete=models.CASCADE,
                               blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", related_name="reviews", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'{self.message[:10]}, {self.author}'


    def get_answers(self):
        return self.children.all()
