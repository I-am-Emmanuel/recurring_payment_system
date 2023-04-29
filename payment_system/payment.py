import pycash

def activate_payment(amount, email, reference):
    """
    Initiates a payment on Paystack.
    """
    user = pycash.Client(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = client.transaction.initialize(
        amount=amount,
        email=email,
        reference=reference,
        callback_url='http://localhost:8000/api/paystack/callback/'
    )
    return response['data']['authorization_url']