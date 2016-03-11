from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.validators import RegexValidator

REGISTRATION_MESSAGE = {'subject': "Validation mail",
                        'message': 'Please validate Your account under this link http://localhost:8000/en-us/validate/{}',
                        'from': 'test@test.com'}


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                                password=password,
                                name=name
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    VALIDATED_CHOICES = ((0, 'Not validated'), (1, 'Validated'))
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    validated = models.IntegerField(choices=VALIDATED_CHOICES, default=0)
    validation_slug = models.CharField(db_index=True, unique=True, max_length=50)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'password']

    @classmethod
    def register(cls, name, password, email):
        user = cls.objects.filter(email=email).first()
        if not user:
            user = cls.objects.create_user(username=name, email=email, password=password)
            if user:
                user.validation_slug = make_password(None)
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
            return True
        return False

    def is_superuser(self):
        return True

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
    ccv = models.CharField(max_length=4,validators=[RegexValidator(r'\d{3,4}',_('Wrong CCV number.'))])
    payment_type = models.CharField(max_length=5,default='N')
