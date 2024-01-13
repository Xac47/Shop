from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from multiupload.fields import MultiFileField, MultiImageField

from product.models import Product, ProductImages, Category, Tag, Color, Specifications, Size, Weight, Reviews


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('id', 'gram', 'slug')
    list_display_links = ('id', 'gram', 'slug')
    prepopulated_fields = {'slug': ('gram',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'get_image', 'get_image_svg')
    list_display_links = ('id', 'name', 'slug', 'get_image', 'get_image_svg')
    readonly_fields = ('get_image',)
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="50" height="50">')
        except ValueError:
            return mark_safe(f'<img src={obj.image} width="50" height="50">')

    def get_image_svg(self, obj):
        try:
            return mark_safe(f'<img src={obj.image_svg.url} width="50" height="50">')
        except ValueError:
            return mark_safe(f'<img src={obj.image_svg} width="50" height="50">')

    get_image.short_description = "Изображение"
    get_image_svg.short_description = "Изображение"


class SpecificationsInline(admin.TabularInline):
    model = Specifications
    extra = 0


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 0
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = "Изображение"


class ProductAdminForm(forms.ModelForm):
    # image = MultiImageField(min_num=1, max_num=10)
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    desc = forms.CharField(widget=CKEditorWidget())

    class Meta:
        # fields = '__all__'
        exclude = ('slug',)
        model = Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'status', 'category', 'price', 'author', 'get_image')
    list_display_links = ('id', 'title', 'slug', 'status', 'category', 'price', 'author', 'get_image')
    readonly_fields = ('get_image',)
    form = ProductAdminForm
    inlines = (ProductImagesInline, SpecificationsInline)
    # prepopulated_fields = {'slug': ('title',)}
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50">')

    get_image.short_description = "Изображение"


admin.site.register(Specifications)
admin.site.register(Reviews)
