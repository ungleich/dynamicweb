from django import forms


from utils.forms import LoginFormMixin


class LoginForm(LoginFormMixin):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
