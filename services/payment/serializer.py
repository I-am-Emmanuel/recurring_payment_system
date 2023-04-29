from rest_framework import serializers
from . models import InitiatePaymentSystem

from django.core.validators import MaxLengthValidator, MinLengthValidator

import secrets

class VerifyMyAccountSerializer(serializers.Serializer):
    
    account_number = serializers.CharField(max_length=10, validators = [MinLengthValidator(10, message='Your account should be 10 digit numbers'), MaxLengthValidator(10)], required=True )
    bank_code = serializers.CharField(required=True)

class InitiatePaymentSerializer(serializers.ModelSerializer):
    
    
    class Meta:  
        model = InitiatePaymentSystem
        fields = ['id','email','amount', 'card_number', 'cvv', 'expiry_month', 'expiry_year', 'subscription_plan']
        read_only_fields = ('id', 'created_at', 'user')


    def create(self, validated_data):
        transaction_reference = validated_data.pop('transaction_reference', None)
        details = self.Meta.model(**validated_data)
        while not transaction_reference:
            details.transaction_reference = secrets.token_urlsafe(50)
            similar_transaction = InitiatePaymentSystem.objects.filter(transaction_reference=details.transaction_reference)
        if not similar_transaction:
            details.transaction_reference = details.transaction_reference
        details.save()
        return details


        # def create(self, validated_data):
        # password = validated_data.pop('password', None)
        # details = self.Meta.model(**validated_data)
        # details.email = details.email
        # # details.otp = details.otp(sendOtp(email=details.email))
        # if password is not None:
        #     details.set_password(password)
        # details.save()
        # return details