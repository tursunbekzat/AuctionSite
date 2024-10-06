from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Product


@login_required
def my_profile(request):
    user = request.user  # Текущий залогиненный пользователь
    return render(request, 'profile/my_profile.html', {'user': user})


@login_required
def my_auctions(request):
    auctions = Product.objects.filter(author=request.user)
    return render(request, 'profile/my_auctions.html', {'auctions': auctions})


    