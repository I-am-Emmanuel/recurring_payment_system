from rest_framework import serializers
from . models import PaymentModel

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth import get_user_model
from background_task.models import Task

import secrets

class VerifyMyAccountSerializer(serializers.Serializer):
    
    account_number = serializers.CharField(max_length=10, validators = [MinLengthValidator(10, message='Your account should be 10 digit numbers'), MaxLengthValidator(10)], required=True )
    bank_code = serializers.CharField(required=True)

class CardDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ['card_first_six_digit']
        read_only_fields = ['country_code', 'card_type', 'bank_name', 'card_last_four_digit', 'ccv', 'expiry_month', 'expiry_year',]



class InitializeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ['id', 'amount','email', 'authorization_code', 'subscription_plan', 'payment_interval', 'card_type', 'card_first_six_digit', 'card_last_four_digit',\
                 'ccv', 'expiry_month', 'expiry_year']
        read_only_fields=['authorization_code', 'customer']

class PaymentSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields =['created_time', 'authorization_code', 'amount', 'email']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        







