from django.shortcuts import render

# Create your views here.
# views.py
import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_items = data.get('cartItems', [])
        total_price = data.get('totalPrice', 0)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': item['name'],
                            },
                            'unit_amount': int(item['price'] * 100),  # price in cents
                        },
                        'quantity': item['quantity'],
                    } for item in cart_items
                ],
                mode='payment',
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/cancel',
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
