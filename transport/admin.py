from django.contrib import admin

from .models import User, Response, Pay_method, Category, Type, Additional, Transport, Deal

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone" ,'email')

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', "rating", "author", "timestamp")

class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'rent_transport', 'owner', 'client', 'start_date', 'close_date', 'total_price', 'pay_method')

class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'category', 'type', 'photo', 'price_per_day')

admin.site.register(User, UserAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Pay_method)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Additional)
admin.site.register(Transport, TransportAdmin)
