from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from decimal import Decimal as dec

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . models import InitiatePaymentSystem
from .serializer import InitiatePaymentSerializer, VerifyMyAccountSerializer
import requests
from django.conf import settings


class VerifyMyAccount(APIView):
    serializer_class = VerifyMyAccountSerializer
    
    def post(self, request):
        data = request.data # access the first (and only) element of the data list
        account_number = data.get("account_number")
        bank_code = data.get("bank_code")
        
        url = "https://api.paystack.co/bank/resolve"
        headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url=url, headers=headers, params={"account_number": account_number, "bank_code": bank_code})
            # print(response.json())
            if response.status_code == 200:
                account_name = response.json()["data"]["account_name"]
                return Response({"account_name": account_name})
            else:
                return Response({"error": "Failed to verify account number"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class InitiatePaymentView(generics.GenericAPIView):
#     serializer_class = InitiatePaymentSerializer

class InitiatePaymentView(generics.GenericAPIView):
    queryset = InitiatePaymentSystem
    serializer_class = InitiatePaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Make payment request to Paystack API
        response = requests.post('https://api.paystack.co/charge',
                                 headers={
                                     'Authorization': 'Bearer YOUR_SECRET_KEY',
                                     'Content-Type': 'application/json'
                                 },
                                 json={
                                     'email': data['email'],
                                     'amount': int(data['amount'] * 100),
                                     'card': {
                                         'number': data['card_number'],
                                         'cvv': data['cvv'],
                                         'expiry_month': data['expiry_month'],
                                         'expiry_year': data['expiry_year']
                                     }
                                 })

        if response.status_code == 200:
            # Payment successful, update your database here
            return Response({'status': 'success', 'amount': data['amount']}, status=status.HTTP_200_OK)
        else:
            # Payment failed
            return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Return a list of all successful payments
        payments = InitiatePaymentSystem.objects.all()
        serializer = InitiatePaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)