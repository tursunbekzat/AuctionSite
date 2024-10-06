from django.urls import path
from . import views

urlpatterns = [
    path('my-profile/', views.my_profile, name='my_profile'),
    path('my-auctions/', views.my_auctions, name='my_auctions'),
    path('my-bids/', views.my_bids, name='my_bids'),
]
