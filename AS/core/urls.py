from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('auctions/', current_auctions_view, name='current_auctions'),
    path('auction/create/', create_auction_view, name='create_auction'),
    path('auction/<int:product_id>/', make_bid_view, name='auction_detail'),
]
