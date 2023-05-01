from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
import secrets



# Create your models here.

class PaymentModel(models.Model):
    # customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=False)
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
    
    class Meta:
        def __str__(self) -> str:
            return f'{self.authorization_code} {self.customer.username} {self.customer.email} {self.amount}\
                 {self.interval}, {self.created_time}'

        ordering = ['-created_time']
        permissions = [
            ('view_history', 'Can view history')
        ]



# class ScheduledPayment(models.Model):
#     customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_interval = models.CharField(max_length=10, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])
#     next_payment_date = models.DateField()
#     created_time = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         def __str__(self) -> str:
#             return f'{self.customer.username} {self.customer.email} {self.amount} {self.interval}, {self.created_time}'

#         ordering = ['-created_time']
#         permissions = [
#             ('view_history', 'Can view history')
#         ]


    

# class InitiatePaymentSystem(models.Model):
#     PAYMENT_CHOICES = (
#         ('W', 'WEEKLY'),
#         ('M', 'MONTHLY'),
#         ('Y', 'YEARY'),
#     )
#     # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     card_number = models.CharField(max_length=19)
#     cvv = models.CharField(max_length=4)
#     expiry_month = models.CharField(max_length=2)
#     expiry_year = models.CharField(max_length=4)
#     transaction_reference = models.CharField(max_length=200, unique=True)
#     email = models.EmailField(blank=True)
#     is_verified = models.BooleanField(default=False)
#     created_time = models.DateTimeField(auto_now_add=True)
#     subscription_plan = models.CharField(max_length=1, choices=PAYMENT_CHOICES, null=True, blank=False)

    

#     class Meta:
#         ordering = ('-created_time',)

#     def __str__(self) -> str :
#         return f' {self.email}'

#     def amount_value(self) -> int:
#         return self.amount *100

    # def first_name(self) -> str:
    #     return self.user.first_name

    # def last_name(self) -> str:
    #     return self.user.last_name



