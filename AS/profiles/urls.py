from django.urls import path
from .views import *

urlpatterns = [
    path('my-profile/', my_profile, name='my_profile'),
    path('my-auctions/', my_auctions, name='my_auctions'),
    path('my-bids/', my_bids, name='my_bids'),
    path('auctions/<int:auction_id>/update/', update_auction_view, name='update_auction'),
    path('auctions/<int:auction_id>/delete/', delete_auction_view, name='delete_auction'),
    path('auctions/<int:auction_id>/extend/', extend_auction_view, name='extend_auction'),
]
