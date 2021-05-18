from django.contrib import admin

from .models import User, Category, Transport

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display= ("id", "username", "phone" ,'email')

admin.site.register(User, UserAdmin)
