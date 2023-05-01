from rest_framework import serializers
from . models import PaymentModel

from django.contrib.auth import get_user_model



class InitializeTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ['id', 'amount','email', 'authorization_code', 'subscription_plan', 'payment_interval', 'card_type', 'card_first_six_digit', 'card_last_four_digit',\
                 'ccv', 'expiry_month', 'expiry_year']
        read_only_fields=['authorization_code']

        # def create(self, validated_data):
        #     user_id = validated_data.pop('customer', None)
        #     if user_id:
        #         validated_data['customerer_id'] = user_id
        #     return super().create(validated_data)


class PaymentSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields =['status', 'created_time', 'authorization_code', 'amount', 'email']



        







