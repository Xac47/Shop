from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import Order

from .tasks import order_created


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):

    def get_queryset(self):
        user = self.request.user
        return user.orders.all()


def order_detail(request, order_id):
    user = request.user
    order = user.orders.get(id=order_id)
    order_items = order.items.all()
    return render(request, 'orders/order_detail.html',
                  {'order': order, 'order_items': order_items})


@login_required()
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST' and cart.__len__():
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['total_price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            # order_created.delay(order.id)
            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
