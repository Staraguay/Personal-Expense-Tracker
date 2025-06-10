from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from defaultFields.models import DefaultModel
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Transaction(DefaultModel):
    CATEGORY = [('Groceries', 'Groceries'), ('Party', 'Party'), ('Food', 'Food'), ('Cinema', 'Cinema'),
                ('Transportation', 'Transportation'), ('Study', 'Study'), ('Clothing', 'Clothing'), ('Fun', 'Fun'),
                ('Mobil plan', 'Mobile plan'), ('Rent', 'Rent'), ('Snacks', 'Snacks'), ('Salary', 'Salary')]
    TYPE = [('Incomings','Incomings'), ('Expenses','Expenses')]
    PAYMENT_TYPE = [('Credit Card EC', 'Credit Card EC'), ('Debit Card CAD', 'Debit Card CAD'), ('Debit Card EC','Debit Card EC'), ('Bank Transfer EC', 'Bank Transfer EC')]
    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    value_cad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    shop = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(verbose_name='date', null=False, blank=False)
    transaction_type = models.CharField(max_length=50, choices=TYPE, verbose_name='type', null=False, blank=False)
    category = models.CharField(max_length=50, choices=CATEGORY, verbose_name='category', null=False, blank=False)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE, verbose_name='payment type', null=False,
                                    blank=False)
    isd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_ec = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class MoneyTransfer(DefaultModel):
    platform = models.CharField(max_length=100, null=False, blank=False)
    usd_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    commission = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    cad_value = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    date = models.DateTimeField(verbose_name='date', null=False, blank=False)
    change_rate = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    processing_days = models.IntegerField(verbose_name='Processing days', null=False, blank=False)
    isd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Profile(models.Model):
    CURRENCY = [('USD','USD')]
    job_position = models.CharField(max_length=100, verbose_name='job position', null=True, blank=True)
    main_currency = models.CharField(max_length=10, choices=CURRENCY, verbose_name='main currency', null=False,
                                     blank=False)
    age = models.IntegerField(verbose_name='age', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='profile')
