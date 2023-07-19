import paypalrestsdk
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def create_payment(request):

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{
                "credit_card": {
                    "type": "visa",
                    "number": "4111111111111111",
                    "expire_month": "12",
                    "expire_year": "2023",
                    "cvv2": "123",
                    "first_name": "John",
                    "last_name": "Doe"
                }
            }]
        },
        "transactions": [{
            "amount": {
                "total": "8.00",
                "currency": "USD"
            },
            "description": "Payment description"
        }]
    })

    if payment.create():
        approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
        return HttpResponseRedirect(approval_url)
    else:
        return HttpResponse("Error creating PayPal payment")


def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Обработка успешного платежа
        return HttpResponse("Payment executed successfully")
    else:
        return HttpResponse("Error executing PayPal payment")