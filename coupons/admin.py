from django.contrib import admin

from coupons.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'is_active']
    list_display_links = ['code', 'valid_from', 'valid_to', 'discount']
    list_filter = ['is_active']