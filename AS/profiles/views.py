from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.forms import ProductForm
from core.models import Product

@login_required
def my_profile(request):
    user = request.user  # Текущий залогиненный пользователь
    return render(request, 'profiles/my_profile.html', {'user': user})


@login_required
def my_auctions(request):
    auctions = Product.objects.filter(author=request.user)
    context = {
        'auctions': auctions,
        'title': 'My Auctions',
        'no_auctions': 'You have not created any auctions yet.',
    }
        
    return render(request, 'core/auctions.html', context)


@login_required
def my_bids(request):
    auctions = Product.objects.filter(bids__user=request.user).distinct()
    context = {
        'auctions': auctions,
        'title': 'My Bids',
        'no_auctions': 'You have not placed any bids yet.',
    }
    return render(request, 'core/auctions.html', context)


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