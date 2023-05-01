from django.contrib import admin
from . models import *



@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['authorization_code', 'email', 'amount', 'subscription_plan', 'payment_interval']
    