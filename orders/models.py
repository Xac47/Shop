from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField('Почтовый индекс', max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField('Оплаченный', default=False)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

