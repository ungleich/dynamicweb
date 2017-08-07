import datetime

from django import forms
from membership.models import CustomUser
from django.contrib.auth import authenticate

from django.utils.translation import ugettext_lazy as _

from .models import UserHostingKey


def generate_ssh_key_name():
    return 'dcl-generated-key-' + datetime.datetime.now().strftime('%m%d%y%H%M')


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
            raise forms.ValidationError(
                _("Your username and/or password were incorrect."))
        elif is_auth.validated == 0:
            raise forms.ValidationError(
                _("Your account is not activated yet."))
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
    private_key = forms.CharField(widget=forms.HiddenInput(), required=False)
    public_key = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form_public_key', 'placeholder': _('Paste here your public key')}),
        required=False,
    )
    user = forms.models.ModelChoiceField(queryset=CustomUser.objects.all(),
                                         required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form_key_name', 'placeholder': _('Give a name to your key')}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserHostingKeyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _('Key name')

    def clean_name(self):
        return self.data.get('name')

    def clean_user(self):
        return self.request.user

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'generate' in self.request.POST:
            self.cleaned_data['name'] = generate_ssh_key_name()
            private_key, public_key = UserHostingKey.generate_keys()
            cleaned_data.update({
                'private_key': private_key,
                'public_key': public_key
            })

        return cleaned_data

    class Meta:
        model = UserHostingKey
        fields = ['user', 'name', 'public_key']
