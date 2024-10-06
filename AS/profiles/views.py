from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from core.forms import ProductForm
from core.models import Product, Bid
from .forms import BidForm

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


# Изменение ставки
@login_required
def edit_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем, что текущий пользователь является автором ставки
    if bid.user != request.user:
        raise PermissionDenied("Вы не можете редактировать чужие ставки.")

    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('my_bids')  # Перенаправляем на страницу с вашими ставками
    else:
        form = BidForm(instance=bid)

    return render(request, 'profiles/edit_bid.html', {'form': form, 'bid': bid})

# Удаление ставки
@login_required
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    # Проверяем, что текущий пользователь является автором ставки
    if bid.user != request.user:
        raise PermissionDenied("Вы не можете удалять чужие ставки.")

    if request.method == 'POST':
        bid.delete()
        return redirect('my_bids')  # Перенаправляем на страницу с вашими ставками

    return render(request, 'profiles/delete_bid.html', {'bid': bid})


@login_required
def update_auction_view(request, auction_id):
    auction = get_object_or_404(Product, id=auction_id, author=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('my_auctions')
    else:
        form = ProductForm(instance=auction)

    return render(request, 'profiles/update_auction.html', {'form': form, 'auction': auction})


@login_required
def delete_auction_view(request, auction_id):
    auction = get_object_or_404(Product, id=auction_id, author=request.user)
    auction.delete()
    return redirect('my_auctions')


@login_required
def extend_auction_view(request, auction_id):
    auction = get_object_or_404(Product, id=auction_id, author=request.user)

    if request.method == 'POST':
        additional_days = int(request.POST.get('additional_days', 0))
        if additional_days > 0:
            auction.extend_auction(additional_days)
            return redirect('my_auctions')

    return render(request, 'profiles/extend_auction.html', {'auction': auction})