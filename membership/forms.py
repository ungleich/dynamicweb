__author__ = 'tomislav'
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password','type':'password'}))


class RegisterForm(LoginForm):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter name'}))
