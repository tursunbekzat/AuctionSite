import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Product
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Создаем платежное намерение
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.current_price * 100),  # Stripe работает с ценами в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
        )
        payment = Payment.objects.create(
            user=request.user,
            product=product,
            amount=product.current_price,
            stripe_payment_intent=session.payment_intent,
            status='pending'
        )
        return JsonResponse({'session_id': session.id})

    return render(request, 'payment/checkout.html', {'product': product})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status': 'invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent = session['payment_intent']

        try:
            payment = Payment.objects.get(stripe_payment_intent=payment_intent)
            payment.status = 'completed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'}, status=200)
