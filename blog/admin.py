from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Posts

admin.site.register(Posts)

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'username', 'bio', 'created_at', 'is_staff'
    )