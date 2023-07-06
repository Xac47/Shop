from decimal import Decimal
from django.conf import settings
from product.models import Product
from coupons.models import Coupon


class Cart:

    def __init__(self, session, cart_storage):
        self.session = session
        self.cart_storage = cart_storage
        self.coupon_id = None

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        self.cart_storage.add_product(
            product_id=product_id,
            price=str(product.price),
            quantity=quantity,
            update_quantity=update_quantity
        )
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        self.cart_storage.remove_product(product_id=product_id)
        self.save()

    def get_items(self):
        items = self.cart_storage.get_all_products()
        products = Product.objects.filter(id__in=[item['product_id'] for item in items])
        for item in items:
            item['product'] = next(p for p in products if str(p.id) == item['product_id'])
            yield item

    def clear(self):
        self.cart_storage.clear()
        self.save()

    def apply_coupon(self, coupon_code):
        coupon = Coupon.objects.filter(code=coupon_code).first()
        if not coupon:
            return False  # неверный купон
        self.coupon_id = coupon.id
        self.save()
        return True

    def get_total_price(self):
        items = self.cart_storage.get_all_products()
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in items)
        return total_price

    def get_discount(self):
        if not self.coupon_id:
            return Decimal('0')
        coupon = Coupon.objects.filter(id=self.coupon_id).first()
        if not coupon:
            return Decimal('0')  # неверный купон
        discount = (coupon.discount / Decimal('100')) * self.get_total_price()
        return discount

    def get_total_price_after_discount(self):
        total_price = self.get_total_price()
        discount = self.get_discount()
        total_price_after_discount = total_price - discount
        return total_price_after_discount

    def save(self):
        self.cart_storage.save_cart_to_session(session=self.session, cart_id=settings.CART_SESSION_ID,
                                               coupon_id=self.coupon_id)


class CartStorage:

    def __init__(self, session):
        self.session = session

    def add_product(self, product_id, price, quantity, update_quantity=False):
        cart = self.session.get(settings.CART_SESSION_ID, {})
        if product_id not in cart or not update_quantity:
            cart[product_id] = {'quantity': 0}
        cart[product_id]['quantity'] += quantity
        cart[product_id]['price'] = price
        self.session[settings.CART_SESSION_ID] = cart

    def remove_product(self, product_id):
        cart = self.session.get(settings.CART_SESSION_ID, {})
        if product_id in cart:
            del cart[product_id]
            self.session[settings.CART_SESSION_ID] = cart

    def get_all_products(self):
        cart = self.session.get(settings.CART_SESSION_ID, {})
        items = [{'product_id': k, 'quantity': v['quantity'], 'price': v['price']} for k, v in cart.items()]
        return items

    def clear(self):
        del self.session[settings.CART_SESSION_ID]

    def save_cart_to_session(self, session, cart_id, coupon_id=None):
        session[cart_id] = {
            'items': self.get_all_products(),
            'coupon_id': coupon_id
        }
        session.modified = True
