from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Product, Bid


@login_required
def my_profile(request):
    user = request.user  # Текущий залогиненный пользователь
    return render(request, 'profiles/my_profile.html', {'user': user})


@login_required
def my_auctions(request):
    auctions = Product.objects.filter(author=request.user)
    return render(request, 'profiles/my_auctions.html', {'auctions': auctions})


@login_required
def my_bids(request):
    bids = Bid.objects.filter(user=request.user)
    return render(request, 'profiles/my_bids.html', {'bids': bids})