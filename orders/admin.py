from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_display_links = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
