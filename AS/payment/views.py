import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Product
from payment.models import Payment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def top_up_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                # Создаем платеж для пополнения баланса
                payment = Payment.objects.create(
                    user=request.user,
                    amount=float(amount),
                    status='pending'  # Измените статус после обработки платежа
                )
                # Логика реальной обработки платежа здесь (интеграция с платежной системой)

                # Предположим, что оплата прошла успешно
                payment.status = 'completed'
                payment.save()

                # Обновляем баланс пользователя
                request.user.balance += payment.amount
                request.user.save()

                messages.success(request, 'Ваш баланс успешно пополнен.')
                return redirect('check_balance')

            except Exception as e:
                messages.error(request, 'Произошла ошибка при пополнении баланса.')
    
    return render(request, 'payments/top_up_balance.html')


@login_required
def check_balance(request):
    # Отображаем текущий баланс пользователя
    balance = request.user.balance
    transactions = Payment.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'balance': balance,
        'transactions': transactions
    }

    return render(request, 'payments/check_balance.html', context)


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
