from django.contrib import admin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'country', 'is_superuser')
    list_filter = ('email', 'country', 'is_superuser')


admin.site.register(CustomUser, CustomUserAdmin)