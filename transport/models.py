from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import os
from django.core.validators import MaxValueValidator, MinValueValidator

# For img resize
from PIL import Image


def transport_directory_path(instance, filename):
    return "owner_{0}/{1}".format(instance.owner.pk, filename)

def image_format_validator(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png','.jpg']
    if not ext in valid_extensions:
        raise ValidationError(u'Need png or jpg image to be uploaded')

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    adress = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=500, blank=True, null=True)
    datestamp = models.DateField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return f"{self.pk}.{self.username}.{self.email}.{self.phone}"
    
class Response(models.Model):
    text = models.TextField(max_length=500, blank=True, null=True)
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writed_responses")
    on_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="received_responses")
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.pk}.{self.author.username}.{self.rating}.{self.timestamp}.{self.text.split()[0]}"
    def is_valid_response(self):
        return self.author != self.on_user

class Pay_method(models.Model):
    pay_method_name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.pk}.{self.pay_method_name}"

class Category(models.Model):
    category_name = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.pk}. {self.category_name}"
 
class Type(models.Model):
    type_name = models.CharField(max_length=40)
    def __str__(self):
        return f"{self.pk}. {self.type_name}"

class Additional(models.Model):
    add_name = models.CharField(max_length=50)
    add_price = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    def __str__(self):
        return f"{self.pk}_{self.add_name}.{self.add_price}"

class Transport(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="transports")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name="transports")
    passenger_places = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    baggage_places = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    air_conditioner = models.CharField(max_length=4,null=True, blank=True)
    automat_gearbox = models.CharField(max_length=10, null=True, blank=True)
    price_per_day = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_transport")
    clients = models.ManyToManyField(User, blank=True, related_name="rented_transport")
    photo = models.ImageField(default='default.png', upload_to=transport_directory_path, blank=True, validators=[image_format_validator])
    pick_up_location = models.CharField(max_length=100, null=True, blank=True,)
    timestamp = models.DateTimeField(auto_now_add=True)
    in_users_lists = models.ManyToManyField(User, blank=True, related_name="transports_in_list")
    def __str__(self):
        return f"{self.pk}.{self.name}.{self.price_per_day}.Clients: {self.clients.all().count()}"
    def is_valid_transport(self):
        return self.owner not in self.clients.all()
    def save(self):
        super().save()  # saving image first
        img = Image.open(self.photo.path) # Open image using self
        img.thumbnail((300,250))
        img_w, img_h = img.size
        background = Image.new(mode = "RGB", size = (300, 250))
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(img, offset)
        background.save(self.photo.path)
    

class Deal(models.Model):
    rent_transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name="deals")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="give_deals")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rent_deals")
    start_date = models.DateField()
    close_date = models.DateField()
    deliver_to = models.CharField(max_length=100, null=True, blank=True)
    pick_up_from = models.CharField(max_length=100, null=True, blank=True)
    additionals = models.ManyToManyField(Additional, blank=True, related_name='on_deals')
    total_price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    pay_method = models.ForeignKey(Pay_method, on_delete=models.CASCADE, related_name='deals')
    def __str__(self):
        return f"Owner: {self.owner.username}, Client: {self.client.username}, {self.total_price}, start-{self.start_date}"
    def is_valid_deal(self):
        return (self.owner != self.client) and (self.start_date < self.close_date)
