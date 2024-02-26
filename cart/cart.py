from decimal import Decimal
from django.conf import settings
from product.models import Product
from coupons.models import Coupon


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.get_discount_price())}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            return self.cart[product_id]

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['discount_price'] = self.get_price_discount(item['total_price']) \
                if self.coupon else item['total_price']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        if self.session.get('coupon_id'):
            del self.session['coupon_id']
        self.session.modified = True

    # Купон
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.active.get(id=self.coupon_id)
        return None

    def get_saved_money(self):
        if self.coupon:
            return round((self.get_total_price() * self.coupon.discount) / Decimal('100'), 2)
        return Decimal('0.00')

    def get_price_discount(self, price):
        if self.coupon:
            return price * (100 - self.coupon.discount) / 100
        return price

    # возвращаем общую сумму корзины после вычета суммы скидки
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_saved_money()
