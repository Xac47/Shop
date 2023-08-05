from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from base.models import BaseModel, ImageBaseModel

from base.svgfield import SVGField
from product.managers import ManagerCustom

User = get_user_model()


class Color(BaseModel):
    name = models.CharField('Цвет', max_length=120)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        indexes = [
            models.Index(fields=['name', 'slug'])
        ]

    def __str__(self):
        return str(self.name)


class Category(BaseModel, ImageBaseModel):
    name = models.CharField('Имя', max_length=200, unique=True)
    image = models.ImageField('Фото jpg', upload_to='category_images/%Y/%m/%d/', blank=True, null=True)
    image_svg = SVGField('Фото svg', upload_to='category_images/%Y/%m/%d/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    # Managers

    objects = models.Manager()

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:category', args=(self.slug,))


class Tag(BaseModel):
    name = models.CharField('Name', max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

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
    slug = models.SlugField(max_length=250)

    image = models.ImageField('Изображение', upload_to='product_images/%Y/%m/%d/%H/')
    back_image = models.ImageField('Изображение сзади', upload_to='product_images/%Y/%m/%d/%H/')

    desc = models.TextField('Описание')
    status = models.CharField('Статус', choices=Status.choices, default=Status.DRAFT, max_length=2)

    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    discount = models.SmallIntegerField('Скидка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    # Managers

    objects = models.Manager()
    published = ManagerCustom('PB')
    draft = ManagerCustom('DF')

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at', 'title', 'status'])
        ]
        verbose_name = 'Продук'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_discount_price(self):
        if not self.discount:
            return self.price
        price = self.price * (100 - self.discount) / 100
        return price

    def get_reviews(self):
        return self.reviews.filter(parent__isnull=True)

    def get_absolute_url(self):
        return reverse('product:product_detail', args=(self.category.slug, self.pk, self.slug))


class Specifications(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                   related_name='specifications')
    width = models.IntegerField(verbose_name='Ширина')
    height = models.IntegerField(verbose_name='Высота')
    depth = models.IntegerField(verbose_name='Глубина')
    weight = models.IntegerField(verbose_name='Масса')
    color = models.ManyToManyField(Color)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return f'{self.product}'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')
    image = models.ImageField('Фото', upload_to='product_images/%Y/%m/%d/%H/')
    phote_number = models.SmallIntegerField('Номер фото')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотки'

    def __str__(self):
        return str(self.phote_number)


class Rating(BaseModel):
    STAR = (
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐')
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


class Favorites(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избраный'
        verbose_name_plural = 'Избраные'
        indexes = [
            models.Index(fields=['user', 'product'])
        ]

    def __str__(self):
        return f'{self.user}, {self.product}'
