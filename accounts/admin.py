from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser
    list_display = ('phone', 'name', 'birth_date', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'birth_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'name', 'birth_date', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    search_fields = ('phone', 'name',)
    ordering = ('phone',)

admin.site.register(CustomUser, CustomUserAdmin)
