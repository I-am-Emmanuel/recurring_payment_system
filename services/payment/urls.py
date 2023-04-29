from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import VerifyMyAccount, InitiatePaymentView

# router = DefaultRouter()

# router.register('payments', InitiatePaymentSystem, basename='payment')




urlpatterns = [
    # path('', include(router.urls)),
    path('verify-account/', VerifyMyAccount.as_view(), name='verify-account'),
    path('initiate-payment/', InitiatePaymentView.as_view(), name='initiated'),
    # path('paystack/payment/callback/', PaystackPaymentCallback.as_view(), name='paystack-callback'),

]

# from django.urls import path
# from .views import Payment

# urlpatterns = [
#     path('payments/', Payment.as_view()),
# ]