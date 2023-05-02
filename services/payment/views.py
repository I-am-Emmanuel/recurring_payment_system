from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import HttpResponse

from background_task import background
from background_task.models import Task
from decimal import Decimal as dec
from datetime import timedelta

import time
import datetime
import requests

from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
# from rest_framework.mixins import CreateModelMixin
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from . models import PaymentModel
from . serializer import InitializeTransactionSerializer, PaymentSystemSerializer
from . user_permission import *





            

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

        # ensuring customer who want interval payment subscribe for it
        if data['subscription_plan'] is False and data['payment_interval'] is not None:
            return Response({'message': "If you unchecked your subscription plan,\
                            to can't set a payment interval"}, status=status.HTTP_205_RESET_CONTENT)

        #  ensuring customer who dont want subsription plan end up opt in for it                 
        elif data['subscription_plan'] is True and data['payment_interval'] is None:
            return Response({'message': "You can't select a subscription plan and won't pick a payment plan"}, status=status.HTTP_205_RESET_CONTENT)
            # except Exception as error_message:
            #             return Response({'error_message': str(error_message)})
                
    
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
                    access_code = response_data['data']['access_code']
                    reference = response_data['data']['reference']
                    customer = PaymentModel.objects.create(
                    email=email,
                    amount= amount,
                    subscription_plan=data['subscription_plan'],
                    payment_interval= data['payment_interval'],
                    card_type=data['card_type'],
                    card_first_six_digit= data['card_first_six_digit'],
                    card_last_four_digit=data['card_last_four_digit'],
                    ccv=data['ccv'],
                    expiry_month=data['expiry_month'],
                    expiry_year=data['expiry_year'],
                    authorization_code = reference,
                    status= PaymentModel.PAYMENT_STATUS_FAILED
                    )

                    customer.save()
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    
   
                access_code = response_data['data']['access_code']
                reference = response_data['data']['reference']
                
                # creating an object in the database
                customer = PaymentModel.objects.create(
                    email=email,
                    amount= amount,
                    subscription_plan=data['subscription_plan'],
                    payment_interval= data['payment_interval'],
                    card_type=data['card_type'],
                    card_first_six_digit= data['card_first_six_digit'],
                    card_last_four_digit=data['card_last_four_digit'],
                    ccv=data['ccv'],
                    expiry_month=data['expiry_month'],
                    expiry_year=data['expiry_year'],
                    authorization_code = reference

                ) 
                customer.status = PaymentModel.PAYMENT_STATUS_COMPLETE
                customer.save()# all data collected at the point of payment been saved
                
                # check for reccuring payment
                if customer.subscription_plan:
                    interval = data['payment_interval'].lower()
                    
                    if interval == 'weekly':
                        next_payment = timedelta(days=7).total_seconds()

                    elif interval == 'monthly':
                        next_payment = timedelta(days=30).total_seconds()
                      
                    elif interval == 'yearly':
                        next_payment = timedelta(days=30).total_seconds()

                    # calling for recurring payment if condition is met
                    reccured_payment(customer.pk, repeat=next_payment)
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
        payment.status = PaymentModel.PAYMENT_STATUS_COMPLETE
        payment.save()

    else:
        # Save failed payment
        payment.status = Payment.PAYMENT_STATUS_FAILED
        payment.save()



# this function terminate a running background payment by the customer

@action(detail=True, permission_classes=[IsAuthenticated])
def stop_recurring_payment(request, pk=None):
    
    tasks = Task.objects.filter(task_params__contains=pk)
    for task in tasks:
        task.delete()

    return HttpResponse(f"Stopped automatic payment for user with id {pk}")


class CustomerPaymentHistory(ListAPIView):

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

