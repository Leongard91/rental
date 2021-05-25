from django import forms
from .models import User, Response, Pay_method, Category, Type, Additional, Transport, Deal

CATEGORY_CHOISES = [('0', 'Choose Category')] + [(category.pk, category.category_name) for category in Category.objects.all().order_by('pk')]
TYPE_CHOISES = [('0', 'Choose Type')] + [(type.pk, type.type_name) for type in Type.objects.all().order_by('pk')]
AIR_COND_CHOISES = [('Yes', 'Air Conditioner'), ('No', 'No Air Conditioner')]
GEARBOX_CHOISES = [('Automat', "Gearbox Automat"), ('Manual', "Gearbox Manual")]

class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Usename', 'class': 'form-control'}))
    password = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder' : 'Password', 'class': 'form-control'}))

class NewUserForm(forms.Form):
    username = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Usename', 'class': 'form-control'}))
    password = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder' : 'Password', 'class': 'form-control'}))
    confirmation = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder' : 'Confinrm Password', 'class': 'form-control'}))
    email = forms.EmailField(label='', max_length=80, min_length=5, required=False, widget=forms.EmailInput(attrs={'placeholder' : 'Email', 'class': 'form-control'}))
    phone = forms.CharField(label='', max_length=20, min_length=8, widget=forms.TextInput(attrs={'placeholder' : "Phone Number", 'class': 'form-control'}))

class NewTransportForm(forms.Form):
    name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    description = forms.CharField(label='', max_length=500, widget=forms.Textarea(attrs={'placeholder': 'Description', 'class' : 'form-control'}))
    category = forms.ChoiceField(label='', choices=CATEGORY_CHOISES, widget=forms.Select(attrs={'placeholder': 'Choose Category', 'class': 'form-control'}))
    type = forms.ChoiceField(label='', choices=TYPE_CHOISES, widget=forms.Select(attrs={'placeholder': 'Choose Type', 'class': 'form-control'}))
    passenger_places = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'Passenger Places, person(s)', 'class': 'form-control'}))
    baggage_places = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'placeholder': 'Baggage Places, bag(s)', 'class': 'form-control'}))
    air_conditioner = forms.ChoiceField(label='', choices=AIR_COND_CHOISES, widget=forms.Select(attrs={'placeholder': 'Air Condition', 'class': 'form-control'}))
    automat_gearbox = forms.ChoiceField(label='', choices=GEARBOX_CHOISES, widget=forms.Select(attrs={'placeholder': 'Gearbox', 'class': 'form-control'}))
    price_per_day = forms.DecimalField(label='', max_digits=7, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'Price, USD/day', 'class': 'form-control'}))
    pick_up_location = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Pick-up location (Country, State, City)', 'class': 'form-control'}))
    photo = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'height:20%; pading: 0px;'}))
