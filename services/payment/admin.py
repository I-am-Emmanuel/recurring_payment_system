from django.contrib import admin
from . models import *


# Register your models here.
# @admin.register(InitiatePaymentSystem)
# class InitiatePaymentSystemAdmin(admin.ModelAdmin):
#     list_display = ['transaction_reference', 'amount', 'created_time', 'subscription_plan']


@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['authorization_code', 'email', 'amount', 'subscription_plan', 'payment_interval']
    