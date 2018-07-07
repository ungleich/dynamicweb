from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from utils.mailer import BaseEmail
from utils.mailer import DigitalGlarusRegistrationMailer
from utils.stripe_utils import StripeUtils

REGISTRATION_MESSAGE = {'subject': "Validation mail",
                        'message': 'Please validate Your account under this link '
                                   'http://localhost:8000/en-us/digitalglarus/login/validate/{}',
                        'from': 'test@test.com'}


def get_anonymous_user_instance(CustomUser):
    return CustomUser(name='Anonymous', email='anonymous@ungleich.ch',
                      validation_slug=make_password(None))


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email,name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            validation_slug=make_password(None)
        )
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(email,
                                password=password,
                                name=name,
                                )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_validation_slug():
    return make_password(None)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    VALIDATED_CHOICES = ((0, 'Not validated'), (1, 'Validated'))
    site = models.ForeignKey(Site, default=1)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    validated = models.IntegerField(choices=VALIDATED_CHOICES, default=0)
    # By default, we initialize the validation_slug with appropriate value
    # This is required for User(page) admin
    validation_slug = models.CharField(
        db_index=True, unique=True, max_length=50,
        default=get_validation_slug
    )
    is_admin = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'password']

    @classmethod
    def register(cls, name, password, email, app='digital_glarus',
                 base_url=None, send_email=True, account_details=None):
        user = cls.objects.filter(email=email).first()
        if not user:
            user = cls.objects.create_user(name=name, email=email,
                                           password=password)
            if user:
                if app == 'digital_glarus':
                    dg = DigitalGlarusRegistrationMailer(user.validation_slug)
                    dg.send_mail(to=user.email)
                elif app == 'dcl':
                    dcl_text = settings.DCL_TEXT
                    user.is_active = False
                    if send_email is True:
                        email_data = {
                            'subject': '{dcl_text} {account_activation}'.format(
                                dcl_text=dcl_text,
                                account_activation=_('Account Activation')
                            ),
                            'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
                            'to': user.email,
                            'context': {'base_url': base_url,
                                        'activation_link': reverse(
                                            'hosting:validate',
                                            kwargs={
                                                'validate_slug': user.validation_slug}),
                                        'dcl_text': dcl_text
                                        },
                            'template_name': 'user_activation',
                            'template_path': 'datacenterlight/emails/'
                        }
                        if account_details:
                            email_data['context'][
                                'account_details'] = account_details
                        email = BaseEmail(**email_data)
                        email.send()
                return user
            else:
                return None
        else:
            return None

    @classmethod
    def get_all_members(cls):
        return cls.objects.filter(
            stripecustomer__membershiporder__isnull=False)

    @classmethod
    def validate_url(cls, validation_slug):
        user = cls.objects.filter(validation_slug=validation_slug).first()
        if user:
            user.validated = 1
            user.save()
            return True
        return False

    @classmethod
    def get_random_password(cls):
        return get_random_string(24)

    def is_superuser(self):
        return False

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value


class StripeCustomer(models.Model):
    user = models.OneToOneField(CustomUser)
    stripe_id = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return "%s - %s" % (self.stripe_id, self.user.email)

    @classmethod
    def create_stripe_api_customer(cls, email=None, token=None,
                                   customer_name=None):
        """
            This method creates a Stripe API customer with the given
            email, token and customer_name. This is different from
            get_or_create method below in that it does not create a
            CustomUser and associate the customer created in stripe
            with it, while get_or_create does that before creating the
            stripe user.
        """
        stripe_utils = StripeUtils()
        stripe_data = stripe_utils.create_customer(token, email, customer_name)
        if stripe_data.get('response_object'):
            stripe_cus_id = stripe_data.get('response_object').get('id')
            return stripe_cus_id
        else:
            return None

    @classmethod
    def get_or_create(cls, email=None, token=None):
        """
            Check if there is a registered stripe customer with that email
            or create a new one
        """
        try:
            stripe_utils = StripeUtils()
            stripe_customer = cls.objects.get(user__email=email)
            # check if user is not in stripe but in database
            customer = stripe_utils.check_customer(stripe_customer.stripe_id,
                                                   stripe_customer.user, token)
            if "deleted" in customer and customer["deleted"]:
                raise StripeCustomer.DoesNotExist()
            return stripe_customer
        except StripeCustomer.DoesNotExist:
            user = CustomUser.objects.get(email=email)
            stripe_utils = StripeUtils()
            stripe_data = stripe_utils.create_customer(token, email, user.name)
            if stripe_data.get('response_object'):
                stripe_cus_id = stripe_data.get('response_object').get('id')
                if hasattr(user, 'stripecustomer'):
                    # User already had a Stripe account and we are here
                    # because the account was deleted in dashboard
                    # So, we simply update the stripe_id
                    user.stripecustomer.stripe_id = stripe_cus_id
                    user.stripecustomer.save()
                    stripe_customer = user.stripecustomer
                else:
                    # The user never had an associated Stripe account
                    # So, create one
                    stripe_customer = StripeCustomer.objects.create(
                        user=user, stripe_id=stripe_cus_id
                    )
                return stripe_customer
            else:
                return None


class CreditCards(models.Model):
    name = models.CharField(max_length=50)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=50)
    expiry_date = models.CharField(max_length=50, validators=[
        RegexValidator(r'\d{2}\/\d{4}', _(
            'Use this pattern(MM/YYYY).'))])
    ccv = models.CharField(max_length=4, validators=[
        RegexValidator(r'\d{3,4}', _('Wrong CCV number.'))])
    payment_type = models.CharField(max_length=5, default='N')

    def save(self, *args, **kwargs):
        # override saving to database
        pass


class Calendar(models.Model):
    datebooked = models.DateField()
    user = models.ForeignKey(CustomUser)

    def __init__(self, *args, **kwargs):
        if kwargs.get('datebooked'):
            user = kwargs.get('user')
            kwargs['datebooked'] = datetime.strptime(
                kwargs.get('datebooked', ''), '%d,%m,%Y')
            self.user_id = user.id
        super(Calendar, self).__init__(*args, **kwargs)

    @classmethod
    def add_dates(cls, dates, user):
        old_dates = Calendar.objects.filter(user_id=user.id)
        if old_dates:
            old_dates.delete()
        for date in dates:
            Calendar.objects.create(datebooked=date, user=user)
