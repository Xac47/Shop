from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

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
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
