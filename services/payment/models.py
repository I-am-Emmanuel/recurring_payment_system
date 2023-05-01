from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
import secrets
from services.core.models import User



# Create your models here.

class PaymentModel(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'S'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Success'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    authorization_code = models.CharField(max_length=50)
    subscription_plan = models.BooleanField(default=False)
    payment_interval = models.CharField(max_length=10, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    card_first_six_digit = models.CharField(max_length= 6)
    card_last_four_digit = models.CharField(max_length=4)
    ccv = models.CharField(max_length=3)
    country_code = models.CharField(max_length=4)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    card_type = models.CharField(max_length=11, choices=[('visa', 'Visa'), ('verve', 'Verve'), ('master card', 'Master Card')], null=True, blank=False)
    status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    class Meta:
        def __str__(self) -> str:
            return f'{self.authorization_code} {self.customer.username} {self.email} {self.amount}\
                 {self.interval}, {self.created_time}'

        

        ordering = ['-created_time']
        permissions = [
            ('view_history', 'Can view history')
        ]
