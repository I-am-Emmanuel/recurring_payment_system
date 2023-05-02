# dukka_physical_test
This project is a payment API built with Django Rest Framework for accepting one-time and recurring payments using Paystack payment gateway.

Prerequisites
To run the application, you'll need to have Python 3.x installed on your computer. You will also need to create an account on Paystack to get an API key.

Usage
Authentication
The API uses JWT authentication. To get a token, send a POST request to the /api/token/ endpoint with your username and password in the request body. The response will contain a token field that you can use to make authenticated requests.


Description
This code snippet consists of several classes, views and functions that deal with payment processing. It uses Paystack API to process payment.

InitializeTransactionView
This is a GenericAPIView class that initializes a payment transaction by collecting necessary data required for payment such as email, amount, and payment details. The payment is processed through a POST request to the Paystack API using the collected data. If the payment is successful, a reference code is generated and stored in the database.

If subscription payment is granted by the customer, recurring payment will be scheduled according to the synchronous schedule given by the customer.

Dependencies
This code requires Django, requests, and the Paystack API. It uses Django's rest_framework, background_task, and decimal.

How to Use
Install Django and requests libraries
Ensure you have a Paystack account and set your secret key
Copy and paste this code into a Django app
Update the code with your Paystack secret key
You will also need to install django background task too.
Run the Django app

NAVIGATING THROUGH THE PROJECT
Here are the iist of endpoints of the project;

http://127.0.0.1:8000/auth/users/  This endpoint takes user to the signup page
http://127.0.0.1:8000/auth/jwt/create/ This endpoint create a login parrameter for users. A jwt will be returned together with its refresh token. Grab the token and set at your browser request hearder. Using your browser mod header to set will be advisable. Set the headers: Authorization, Bearer to (JWT <token>) with no parenthesis when creating urs. This is only needed for testing.
http://127.0.0.1:8000/dukka/api/initialize-payment/ This will take user to the payment endpint.
http://127.0.0.1:8000/dukka/api/payments-history/  This endpoint querry all payment made by a user
http://127.0.0.1:8000/dukka/api/stop-payment/   This endpoint authorized a customer to stop a reccuring paymnt. Integer will be use to locate a particular payment history through the url in this case.  
  
