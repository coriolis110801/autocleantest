from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

from captcha.fields import ReCaptchaField


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    captcha = ReCaptchaField()


class ContactForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Message", "rows": 5}
        ),
    )
