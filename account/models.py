from django.contrib.auth.models import User
from django.db import models

from .utility import generate_account_number
from .validators import validate_pin
# from user.models import User
from django.conf import settings


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    pin = models.CharField(max_length = 4, validators = [validate_pin])
    account_number = models.CharField(
        max_length = 10,
        default = generate_account_number,
        unique = True,
        primary_key = True)
    balance = models.DecimalField(max_digits = 15, decimal_places = 2, default = 0.0)

    ACCOUNT_TYPE = [
        ('S', 'SAVINGS'),
        ('C', 'CURRENT'),
        ('D', 'DOM'),
    ]
    account_type = models.CharField(max_length = 1, choices = ACCOUNT_TYPE, default = 's')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.account_type} {self.account_number} {self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deb', 'DEBIT'),
        ('Cre', 'CREDIT'),
        ('TRA', 'TRANSFER')
    ]

    account = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'transactions')
    Transaction_Type = models.CharField(max_length = 3, choices = TRANSACTION_TYPES, default = 'CRE')
    transaction_time = models.DateTimeField(auto_now_add = True)
    date = models.DateField(auto_now = True)
    amount = models.DecimalField(max_digits = 15, decimal_places = 2)
    description = models.TextField(blank = True, null = True)
    TRANSACTION_STATUS = [
        ('S', 'SUCCESSFUL'),
        ('F', 'FAIL'),
        ('P', 'PENDING')
    ]
    transaction_status = models.CharField(max_length = 1, choices = TRANSACTION_STATUS, default = 's')

    def __str__(self):
        return f"{self.id} {self.account} {self.amount} {self.transaction_time} {self.Transaction_Type}"
