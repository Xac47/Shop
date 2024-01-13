from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('id', 'first_name', 'last_name', 'email', 'email_verify', 'is_staff', 'is_active',)
    list_display_links = ('id', 'first_name', 'last_name', 'email', 'email_verify', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'last_name', 'email', 'email_verify', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'image', 'email', 'password')}),
        ('Permissions', {'fields': ('email_verify', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'image', 'email', 'password1', 'password2', 'email_verify', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
