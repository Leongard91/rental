from django import forms

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
    description = forms.CharField(label='', max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Description', 'class' : 'form-control', 'row': 3}))
    # !!!!!!!!!!!!!!!!!!!!!!!!