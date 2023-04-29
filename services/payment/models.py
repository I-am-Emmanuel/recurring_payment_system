from django.db import models
from django.conf import settings
import secrets

# Create your models here.



class InitiatePaymentSystem(models.Model):
    PAYMENT_CHOICES = (
        ('W', 'WEEKLY'),
        ('M', 'MONTHLY'),
        ('Y', 'YEARY'),
    )
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=16)
    cvv = models.CharField(max_length=4)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    transaction_reference = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    subscription_plan = models.CharField(max_length=1, choices=PAYMENT_CHOICES, null=True, blank=False)

    class Meta:
        ordering = ('-created_time',)

    def __str__(self) -> str :
        return f' {self.email}'

    def amount_value(self) -> int:
        return self.amount *100

    # def first_name(self) -> str:
    #     return self.user.first_name

    # def last_name(self) -> str:
    #     return self.user.last_name



