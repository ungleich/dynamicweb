from django import forms
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from datetime import datetime


from utils.models import BillingAddress
from utils.forms import LoginFormMixin, SignupFormMixin, BillingAddressForm

from .models import MembershipType
from .models import Booking


class LoginForm(LoginFormMixin):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(SignupFormMixin):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(label='name',
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}))


class MembershipBillingForm(BillingAddressForm):
    token = forms.CharField(widget=forms.HiddenInput())
    membership_type = forms.ModelChoiceField(queryset=MembershipType.objects.all(),
                                             widget=forms.HiddenInput())

    class Meta:
        model = BillingAddress
        fields = ['membership_type', 'street_address', 'city', 'postal_code', 'country']
        labels = {
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'country': _('Country'),
        }


class BookingBillingForm(BillingAddressForm):
    token = forms.CharField(widget=forms.HiddenInput())
    start_date = forms.DateField(widget=forms.HiddenInput())
    end_date = forms.DateField(widget=forms.HiddenInput())
    price = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = BillingAddress
        fields = ['start_date', 'end_date', 'price', 'street_address',
                  'city', 'postal_code', 'country']
        labels = {
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'country': _('Country'),
        }


class BookingDateForm(forms.Form):
    start_date = forms.DateField(required=False,
                                 widget=forms.TextInput(attrs={'id': 'booking-date-1',
                                                                     'value': ''}))
    end_date = forms.DateField(required=False,
                               widget=forms.TextInput(attrs={'id': 'booking-date-2'}))

    # def clean_date_range(self):
    #     date_range = self.cleaned_data.get('date_range')
    #     dates = date_range.replace(' ', '').split('-')
    #     try:
    #         start_date, end_date = [datetime.strptime(date_string, "%m/%d/%Y").date()
    #                                 for date_string in dates]
    #     except ValueError:
    #         raise forms.ValidationError("Submit valid dates.")

    #     if start_date > end_date:
    #         raise forms.ValidationError("Your end date must be greather than your start date.")

    #     q1 = Q(start_date__lte=start_date, end_date__gte=start_date)
    #     q2 = Q(start_date__gt=start_date, start_date__lte=end_date)
    #     if Booking.objects.filter(q1 | q2).exists():
    #         raise forms.ValidationError("You already have a booking in these dates.")

    #     return start_date, end_date

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("This field is required.")
        # try:
        #     start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
        # except ValueError:
        #     raise forms.ValidationError("Submit valid dates.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if not end_date:
            raise forms.ValidationError("This field is required.")
        return end_date

    def clean(self):

        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if not start_date or not end_date:
            return self.cleaned_data

        if start_date > end_date:
            raise forms.ValidationError("Your end date must be greather than your start date.")

        q1 = Q(start_date__lte=start_date, end_date__gte=start_date)
        q2 = Q(start_date__gt=start_date, start_date__lte=end_date)
        if Booking.objects.filter(q1 | q2).exists():
            raise forms.ValidationError("You already have a booking in these dates.")

        return self.cleaned_data
