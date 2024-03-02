from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem

import csv
import datetime


def export_to_csv(modeladmin, request, queryset):
    ''' Скачивание файлов в формате csv '''
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Напишите первую строку с информацией заголовка
    writer.writerow([field.verbose_name for field in fields])
    # Запись строк данных
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


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

    actions = ['export_to_csv', 'mark_as_paid']

    def export_to_csv(self, request, queryset):
        return export_to_csv(self, request, queryset)

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
