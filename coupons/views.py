from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm

from django.core.exceptions import ObjectDoesNotExist


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.active.get(code__iexact=code,  # поиск совпадения
                                       valid_from__lte=now,  # проверка срока меньше или равными пояс | <=
                                       valid_to__gte=now)  # проверка срока больше или равными поле | >=
            request.session['coupon_id'] = coupon.id
            messages.success(request, f'Купон применен {coupon.discount}%')
        except ObjectDoesNotExist:
            messages.error(request, 'Купон не существует')
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
