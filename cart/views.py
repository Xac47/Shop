from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .cart import Cart, CartStorage

from product.models import Product


def cart_detail(request):
    # Создаем экземпляр класса Cart
    session = request.session
    cart_storage = CartStorage(session)
    cart = Cart(session, cart_storage)

    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    # Получаем продукт по id
    product = Product.published.get(id=product_id)
    # Создаем экземпляр класса Cart
    session = request.session
    cart_storage = CartStorage(session)
    cart = Cart(session, cart_storage)
    # Добавляем продукт в корзину
    cart.add(product=product)
    # Перенаправляем на страницу корзины
    return HttpResponseRedirect(reverse('cart:cart_detail'))


def cart_remove(request, product_id):
    # Получаем продукт по id
    product = Product.published.get(id=product_id)
    # Создаем экземпляр класса Cart
    session = request.session
    cart_storage = CartStorage(session)
    cart = Cart(session, cart_storage)
    # Удаляем продукт из корзины
    cart.remove(product=product)
    # Перенаправляем на страницу корзины
    return HttpResponseRedirect(reverse('cart:cart_detail'))


def cart_clear(request):
    # Создаем экземпляр класса Cart
    session = request.session
    cart_storage = CartStorage(session)
    cart = Cart(session, cart_storage)
    # Очищаем корзину
    cart.clear()
    messages.success(request, "Корзина очищена.")
    # Перенаправляем на страницу корзины
    return HttpResponseRedirect(reverse('cart:cart_detail'))


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        # Создаем экземпляр класса Cart
        session = request.session
        cart_storage = CartStorage(session)
        cart = Cart(session, cart_storage)
        # Применяем купон
        result = cart.apply_coupon(coupon_code=coupon_code)
        if result:
            messages.success(request, "Купон применен успешно.")
        else:
            messages.error(request, "Неверный купон.")
    # Перенаправляем на страницу корзины
    return HttpResponseRedirect(reverse('cart:cart_detail'))
