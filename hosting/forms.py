import datetime
import logging
import subprocess

import tempfile
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from membership.models import CustomUser
from utils.hosting_utils import get_all_public_keys
from .models import UserHostingKey, GenericProduct

logger = logging.getLogger(__name__)


def generate_ssh_key_name():
    return '{prefix}{date_time_str}'.format(
        prefix=settings.DCL_SSH_KEY_NAME_PREFIX,
        date_time_str=datetime.datetime.now().strftime('%m%d%y%H%M%S')
    )


class HostingUserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if self.errors:
            return self.cleaned_data
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
            raise forms.ValidationError(_("User does not exist"))


class ProductModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.product_name


class GenericPaymentForm(forms.Form):
    product_name = ProductModelChoiceField(
        queryset=GenericProduct.objects.all().order_by('product_name'),
        empty_label=_("Choose a product"),
    )
    amount = forms.FloatField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Amount in CHF'),
                   'readonly': 'readonly', }
        ),
        max_value=999999,
        min_value=1,
        label=_('Amount in CHF')
    )
    recurring = forms.BooleanField(required=False,
                                   label=_("Recurring monthly"), )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'style': "height: 60px;"}),
        required=False
    )

    class Meta:
        model = GenericProduct
        fields = ['product_name', 'amount', 'recurring', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if (float(self.cleaned_data.get('product_name').get_actual_price()) !=
                amount):
            raise forms.ValidationError(_("Amount field does not match"))
        return amount

    def clean_recurring(self):
        recurring = self.cleaned_data.get('recurring')
        if (self.cleaned_data.get('product_name').product_is_subscription !=
                (True if recurring else False)):
            raise forms.ValidationError(_("Recurring field does not match"))
        return recurring


class ProductPaymentForm(GenericPaymentForm):
    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        if product_id is not None:
            self.product = GenericProduct.objects.get(id=product_id)
        super(ProductPaymentForm, self).__init__(*args, **kwargs)
        self.fields['product_name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={'placeholder': _('Product name'),
                       'readonly': 'readonly'}
            )
        )
        if self.product.product_is_subscription:
            self.fields['amount'].label = "{amt} ({payment_type})".format(
                amt=_('Amount in CHF'),
                payment_type=_('Monthly subscription')
            )
        else:
            self.fields['amount'].label = "{amt} ({payment_type})".format(
                amt=_('Amount in CHF'),
                payment_type=_('One time payment')
            )
        self.fields['recurring'].widget = forms.HiddenInput()
        self.fields['product_name'].widget.attrs['class'] = 'input-no-border'
        self.fields['amount'].widget.attrs['class'] = 'input-no-border'
        self.fields['description'].widget.attrs['class'] = 'input-no-border'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if (self.product is None or
                float(self.product.get_actual_price()) != amount):
            raise forms.ValidationError(_("Amount field does not match"))
        return amount

    def clean_recurring(self):
        recurring = self.cleaned_data.get('recurring')
        if (self.product.product_is_subscription !=
                (True if recurring else False)):
            raise forms.ValidationError(_("Recurring field does not match"))
        return recurring


class HostingUserSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(label=_("Confirm Password"),
                                       widget=forms.PasswordInput())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': _('Enter your name or company name')}),
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
        attrs={'class': 'form_public_key',
               'placeholder': _('Paste here your public key')}),
        required=False,
    )
    user = forms.models.ModelChoiceField(queryset=CustomUser.objects.all(),
                                         required=False,
                                         widget=forms.HiddenInput())
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form_key_name',
               'placeholder': _('Give a name to your key')}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserHostingKeyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _('Key name')

    def clean_public_key(self):
        """
        Validates a public ssh key using `ssh-keygen -lf key.pub`
        Also checks if a given key already exists in the database and
        alerts the user of it.
        :return:
        """
        if 'generate' in self.request.POST:
            return self.data.get('public_key')
        KEY_ERROR_MESSAGE = _("Please input a proper SSH key")
        openssh_pubkey_str = self.data.get('public_key').strip()

        if openssh_pubkey_str in get_all_public_keys(self.request.user):
            key_name = UserHostingKey.objects.filter(
                user_id=self.request.user.id,
                public_key=openssh_pubkey_str).first().name
            KEY_EXISTS_MESSAGE = _(
                "This key exists already with the name \"%(name)s\"") % {
                                     'name': key_name}
            raise forms.ValidationError(KEY_EXISTS_MESSAGE)

        with tempfile.NamedTemporaryFile(delete=True) as tmp_public_key_file:
            tmp_public_key_file.write(openssh_pubkey_str.encode('utf-8'))
            tmp_public_key_file.flush()
            try:
                subprocess.check_output(
                    ['ssh-keygen', '-lf', tmp_public_key_file.name])
            except subprocess.CalledProcessError as cpe:
                logger.debug(
                    "Not a correct ssh format {error}".format(error=str(cpe)))
                raise forms.ValidationError(KEY_ERROR_MESSAGE)
        return openssh_pubkey_str

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
