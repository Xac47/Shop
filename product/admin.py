from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from product.models import Product, ProductImages, Category, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'get_image')
    list_display_links = ('id', 'name', 'slug', 'get_image')
    readonly_fields = ('get_image',)
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = "Изображение"


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 0
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'status', 'category', 'price', 'author', 'get_image')
    list_display_links = ('id', 'title', 'slug', 'status', 'category', 'price', 'author', 'get_image')
    readonly_fields = ('get_image',)
    inlines = (ProductImagesInline,)
    prepopulated_fields = {'slug': ('title',)}

    save_as = True
    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = "Изображение"
