import random
import string
from django import forms
from membership.models import CustomUser
from django.contrib.auth import authenticate


from utils.stripe_utils import StripeUtils

from .models import HostingOrder, UserHostingKey

class HostingUserLoginForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        is_auth = authenticate(email=email, password=password)
        if not is_auth:
            raise forms.ValidationError("Your username and/or password were incorrect.")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("User does not exist")
        else:
            return email


class HostingUserSignupForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name or company name'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password == password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password


class UserHostingKeyForm(forms.ModelForm):
    private_key = forms.CharField(widget=forms.PasswordInput(), required=False)
    public_key = forms.CharField(widget=forms.PasswordInput(), required=False)
    user = forms.models.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)
    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserHostingKeyForm, self).__init__(*args, **kwargs)
        # self.initial['user'].initial = self.request.user.id
        # print(self.fields)

    def clean_name(self):
        return "dcl-priv-key-%s" % (
            ''.join(random.choice(string.ascii_lowercase) for i in range(7))
        )

    def clean_user(self):
        return self.request.user

    def clean(self):
        cleaned_data = self.cleaned_data

        if not cleaned_data.get('public_key'):
            private_key, public_key = UserHostingKey.generate_keys()
            cleaned_data.update({
                'private_key': private_key,
                'public_key': public_key
            })

        return cleaned_data

    class Meta:
        model = UserHostingKey
        fields = ['user', 'public_key', 'name']
