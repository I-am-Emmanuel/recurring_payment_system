from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.


# class LogoutView(APIView):
#     authentication_classes = (JSONWebTokenAuthentication,)

#     def post(self, request, *args, **kwargs):
#         # Delete the user's token from cookies
#         response = JsonResponse({'detail': 'Successfully logged out'})
#         response.delete_cookie('jwt')
#         return response
