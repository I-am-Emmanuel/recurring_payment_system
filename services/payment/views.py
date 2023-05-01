from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import HttpResponse

from background_task import background
from background_task.models import Task
from decimal import Decimal as dec

import time
import datetime
from datetime import timedelta
import requests


from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
# from rest_framework.mixins import CreateModelMixin
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view

from . models import PaymentModel
from . serializer import  VerifyMyAccountSerializer, InitializeTransactionSerializer, PaymentSystemSerializer, TaskSerializer
from . user_permission import *




class VerifyMyAccount(APIView):
    serializer_class = VerifyMyAccountSerializer
    
    def post(self, request):
        data = request.data # access the first element of the data list
        account_number = data.get("account_number")
        bank_code = data.get("bank_code")
        
        url = "https://api.paystack.co/bank/resolve"
        headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url=url, headers=headers, params={"account_number": account_number, "bank_code": bank_code})
            # print(response.content)
            if response.status_code == 200:
                account_name = response.json()["data"]["account_name"]
                return Response({"account_name": account_name})
            else:
                return Response({"error": "Failed to verify account number"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            return Response({"error": str(error_message)}, status=status.HTTP_400_BAD_REQUEST)

            

# this class initializes transaction and collect all necessary params needed for 
# making the transaction successful, e.g the card details and someother details peculiar to the
# customer's card details. after the first payment has been made, a payment reference will be sent
# to the database, through authorization_code which will be part of what will be needed for further subsequent
# payment if necessary. if subscription payment is granted by the customer, reccuring payment will take in charge
# according to the synchronous schedule been given by the customer
class InitializeTransactionView(generics.GenericAPIView):
    serializer_class = InitializeTransactionSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        email = data['email']
        amount = data['amount']
    
        try:
            if get_user_model().objects.get(email=data['email']):
                url = 'https://api.paystack.co/transaction/initialize'
                headers = {
                    'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    'email': email,
                    'amount': amount,
                    'currency': 'NGN'
                }
                
                response = requests.post(url=url, headers=headers, json=payload)
                response_data = response.json()
                
                if not response.ok:
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                
                access_code = response_data['data']['access_code']
                reference = response_data['data']['reference']
                # print(reference)

                
                # creating an object in the database
                customer = PaymentModel.objects.create(
                    email=email,
                    amount= amount,
                    authorization_code='',
                    subscription_plan=data['subscription_plan'],
                    payment_interval= data['payment_interval'],
                    card_type=data['card_type'],
                    card_first_six_digit= data['card_first_six_digit'],
                    card_last_four_digit=data['card_last_four_digit'],
                    ccv=data['ccv'],
                    expiry_month=data['expiry_month'],
                    expiry_year=data['expiry_year']

                )
                
                customer.authorization_code = reference
                customer.save()# all data collected at the point of payment been saved
                # from datetime import datetime, timedelta

# ...


# ...

                if customer.subscription_plan:
                    interval = data['payment_interval'].lower()
                    # interval = data['payment_interval']
                    if interval == 'weekly'.casefold():
                        next_payment = timedelta(days=7).total_seconds()
                        # datetime.datetime.now()
                        # new_payment = current_time + datetime.timedelta(days=7)
                        # seconds_to_next_payment = (new_payment - current_time).total_seconds()

                    elif interval == 'monthly'.casefold():
                        next_payment = timedelta(days=30).total_seconds()
                        # datetime.datetime.now()
                        # new_payment = current_time + datetime.timedelta(days=30)
                        # seconds_to_next_payment = (new_payment - current_time).total_seconds()

                    elif interval == 'yearly'.casefold():
                        next_payment = timedelta(days=30).total_seconds()
                        # datetime.datetime.now()
                        # new_payment = current_time + datetime.timedelta(days=365)
                        # seconds_to_next_payment = (new_payment - current_time).total_seconds()

                    reccured_payment(customer.pk, repeat=current_time)

 # calling for recurring payment if condition is met


                    
                
                return Response({'access_code': access_code}, status=status.HTTP_201_CREATED)
        except Exception as error_message:
            return Response({'error': str(error_message)}, status=status.HTTP_400_BAD_REQUEST)





    
# this function runs a background task for subsequent payment 
# made by customer, go to @InitializeTransactionView to see how it works
@background(schedule=0)
def reccured_payment(pk=None):
    payment = PaymentModel.objects.filter(pk=pk)

    # Charge authorization
    url = 'https://api.paystack.co/transaction/charge_authorization'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'email': payment.email,
        'amount': payment.amount,
        'authorization_code': payment.authorization_code,
        'bin':payment.card_first_six_digit,
        'last4':payment.card_last_four_digit,
        'ccv':payment.ccv,
        'expiry_month':payment.expiry_month,
        'expiry_year': payment.expiry_year,
        'card_type':payment.card_type,
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        # Save successful payment and create scheduled payment if applicable
        payment.status = Payment.SUCCESS
        payment.save()

    else:
        # Save failed payment
        payment.status = Payment.FAILED
        payment.save()


# @api_view()
# this function terminate a running background payment by the customer

# @action(detail=True, permission_classes=[IsAuthenticated])
# def stop_recurring_payment(self, request, pk=None):
    
#     tasks = Task.objects.filter(task_params__contains=pk)
#     for task in tasks:
#         task.delete()

#     return HtppResponse(f"Stopped automatic payment for user with id {pk}")

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_recurring_payment(request, pk):
    tasks = Task.objects.filter(task_params__contains=pk)
    for task in tasks:
        task.delete()
    return HttpResponse({f"Stopped automatic payment for user with id {pk}"})



class CustomerPaymentHistory(ModelViewSet):

    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSystemSerializer
    
    @action(detail=True, permission_classes=[ViewCustomerPaymentHistoryPermission])
    def history(self, request, pk):
        # Get the customer
        customer = Customer.objects.get(pk=pk)
        # Filter the payments by the customer
        payments = PaymentModel.objects.filter(customer=customer)
        # Serialize the payments
        serializer = self.serializer_class(payments, many=True)
        return Response(serializer.data)


# class StopPayment(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     # @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
#     def stop_recurring_payment(self, request, pk=None):
#         if request.method == 'GET':
#             tasks = Task.objects.filter(task_params__contains=pk)
#             tasks.delete()
#             return Response({f"Stopped automatic payment for user with ID {pk}"}, status=status.HTTP_201_CREATED)

    # def get_serializer_class(self):
    #     if self.action == 'stop_recurring_payment':
    #         return serializers.Serializer
    #     return TaskSerializer



























# class CardValidation(generics.GenericAPIView):
#     serializer_class = CardDetailsSerializers
#     def post(self, request):
        
#         data = request.data
#         data.get('card_first_six_digit')
        
#         url = 'https://api.paystack.co/decision/bin/539983'
#         header = {
#         "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
#         "Content-Type": "application/json"
#         }

#         payload={ 'data': {
#             'bin': data['card_first_six_digit']   
#         }
#         }

#         try:
#             response = requests.get(url=url, headers=header, json=payload)
#             print(response.content)
#             brand = response.json()['data']['brand']
#             # print(response_data)
#             # response_data['data']['authorization']

#             if response.ok:
#                 return Response({'brand': brand}, status=status.HTTP_200_OK)
#             else:
#                 return Response({response_data}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as error_message:
#             return Response({'message': str(error_message)}, status=status.HTTP_400_BAD_REQUEST)










