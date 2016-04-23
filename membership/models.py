from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

REGISTRATION_MESSAGE = {'subject': "Validation mail",
                        'message': 'Please validate Your account under this link http://localhost:8000/en-us/login/validate/{}',
                        'from': 'test@test.com'}


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
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    VALIDATED_CHOICES = ((0, 'Not validated'), (1, 'Validated'))
    site = models.ForeignKey(Site, default=1)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    validated = models.IntegerField(choices=VALIDATED_CHOICES, default=0)
    validation_slug = models.CharField(db_index=True, unique=True, max_length=50)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'password']

    @classmethod
    def register(cls, name, password, email):
        user = cls.objects.filter(email=email).first()
        if not user:
            user = cls.objects.create_user(name=name, email=email, password=password)
            if user:
                send_mail(REGISTRATION_MESSAGE['subject'],
                          REGISTRATION_MESSAGE['message'].format(user.validation_slug),
                          REGISTRATION_MESSAGE['from'], [user.email], fail_silently=False)
                return user
            else:
                return None
        else:
            return None

    @classmethod
    def validate_url(cls, validation_slug):
        user = cls.objects.filter(validation_slug=validation_slug).first()
        if user:
            user.validated = 1
            user.save()
            return True
        return False

    def is_superuser(self):
        return False

    def is_admin(self):
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CreditCards(models.Model):
    name = models.CharField(max_length=50)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=50)
    expiry_date = models.CharField(max_length=50, validators=[RegexValidator(r'\d{2}\/\d{4}', _(
        'Use this pattern(MM/YYYY).'))])
    ccv = models.CharField(max_length=4, validators=[RegexValidator(r'\d{3,4}', _('Wrong CCV number.'))])
    payment_type = models.CharField(max_length=5, default='N')


class Calendar(models.Model):
    datebooked = models.DateField()
    user = models.ForeignKey(CustomUser)

    def __init__(self, *args, **kwargs):
        if kwargs.get('datebooked'):
            user = kwargs.get('user')
            kwargs['datebooked'] = datetime.strptime(kwargs.get('datebooked', ''), '%d,%m,%Y')
            self.user_id = user.id
        super(Calendar, self).__init__(*args, **kwargs)

    @classmethod
    def add_dates(cls,dates,user):
        old_dates = Calendar.objects.filter(user_id=user.id)
        if old_dates:
            old_dates.delete()
        for date in dates:
            Calendar.objects.create(datebooked=date,user=user)

