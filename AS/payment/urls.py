from django.urls import path
from payment import views

urlpatterns = [
    path('checkout/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
