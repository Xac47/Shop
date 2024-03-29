from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    else:
        cart.add(product=product)
    return redirect('cart:cart_detail')


def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            for item in cart:
                if str(item['product'].id) == str(cd['product'].id):
                    if cd['update']:
                        item['quantity'] = cd['quantity']
                    break
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True}
        )
    coupon_apply_form = CouponApplyForm()  # Подключаем систему купонов
    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')
