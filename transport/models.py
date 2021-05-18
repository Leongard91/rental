from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING, SET_NULL
from django.db.models.fields import DurationField, related


def transport_directory_path(instance, filename):
    return "transport_{0}/{1}".format(instance.pk, filename)

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.pk}.{self.username}.{self.email}.{self.phone}"
    
class Response(models.Model):
    text = models.TextField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(min=1, max=5)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.pk}.{self.client.username}.{self.rating}.{self.timestamp}.{self.text.split()[0]}"

class Pay_method(models.Model):
    pay_method_name = models.CharField(max_length=20)

class Category(models.Model):
    category_name = models.CharField(max_length=20)

class Type(models.Model):
    type_name = models.CharField(max_length=20)

class Additional(models.Model):
    add_name = models.CharField(max_length=50)
    add_price = models.DecimalField(null=True, max_digits=7, decimal_places=2)

class Transport(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="transports")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name="transports")
    price_per_day = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    client_responses_on_author = models.ManyToManyField(Response, blank=True, related_name="on_transport")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_transport")
    clients = models.ManyToManyField(User, blank=True, related_name="rented_transport")
    photo = models.ImageField(default='default.png', upload_to=transport_directory_path, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    in_users_lists = models.ManyToManyField(User, blank=True, related_name="transports_in_list")

class Deal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="own_transport")
    client = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="own_transport")
    start_date = models.DateField()
    close_date = models.DateField()
    additionals = models.ManyToManyField(Additional, blank=True, related_name='on_deals')
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    pay_method = models.ForeignKey(Pay_method, on_delete=DO_NOTHING, related_name='deal')
