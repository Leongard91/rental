from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Usename'}))
    password = forms.CharField(max_length=40, widgets=forms.PasswordInput(attrs={'placeholder' : 'Password'}))

class NewUserForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Usename'}))
    password = forms.CharField(max_length=40, widgets=forms.PasswordInput(attrs={'placeholder' : 'Password'}))
    confirmation = forms.CharField(max_length=40, widgets=forms.PasswordInput(attrs={'placeholder' : 'Confinrm Password'}))
    email = forms.EmailField(max_length=80, min_length=5, required=False, widgets=forms.EmailInput(attrs={'placeholder' : 'Email'}))
    phone = forms.CharField(max_length=20, min_length=8, widget=forms.TextInput(attrs={'placeholder' : "Phone Number"}))