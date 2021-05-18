from django.contrib import admin

from .models import User, Response, Pay_method, Category, Type, Additional, Transport, Deal

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone" ,'email')

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', "rating", "client", "timestamp")

admin.site.register(User, UserAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Deal)
admin.site.register(Pay_method)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Additional)
admin.site.register(Transport)
