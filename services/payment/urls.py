from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import VerifyMyAccount, InitializeTransactionView,  CustomerPaymentHistory, stop_recurring_payment
from django.views.generic import TemplateView
# from rest_framework.routers import DefaultRouter


app_name= 'services.payment'

    

router = DefaultRouter()

router.register('customer/payments', CustomerPaymentHistory, basename='payment')
# router.register('stop-reccuring-payment', StopPayment, basename='stop/payment')




urlpatterns = [
    path('', include(router.urls)),
    path('verify-account/', VerifyMyAccount.as_view(), name='verify-account'),
    path('initialize-payment/', InitializeTransactionView.as_view(), name='initialise_payment'),

    # path('stop-reccuring-payment/<int:pk>/', TemplateView.as_view(template_name='payment/customer_payment.html')),
    path('stop_payment/<int:pk>/', stop_recurring_payment, name='stop_payment'),
    # other URL patterns


]

