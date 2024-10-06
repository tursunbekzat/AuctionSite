# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from django.contrib.auth.decorators import login_required
from .forms import ProductForm 
from django.core.exceptions import ValidationError


def home(request):
    return render(request, 'core/index.html')


def current_auctions_view(request):
    # Получаем все аукционы (продукты), у которых есть активные ставки
    auctions = Product.objects.filter(bids__isnull=False).distinct().order_by('-created_at')
    
    context = {
        'auctions': auctions
    }
    
    return render(request, 'core/current_auctions.html', context)


@login_required
def create_auction_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.author = request.user  # Присваиваем текущего пользователя как автора
            auction.save()
            return redirect('current_auctions')
    else:
        form = ProductForm()

    return render(request, 'core/create_auction.html', {'form': form})


@login_required
def make_bid_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')

        if bid_amount:
            try:
                # Создаем новую ставку
                bid = Bid(
                    product=product,
                    user=request.user,
                    amount=float(bid_amount)
                )
                bid.save()

                # Обновляем текущую цену аукциона
                product.current_price = bid.amount
                product.save()

                return redirect('auction_detail', product_id=product.id)

            except ValidationError as e:
                # Показываем сообщение об ошибке в шаблоне
                return render(request, 'core/auction_detail.html', {
                    'product': product,
                    'error': e.message
                })

    return render(request, 'core/auction_detail.html', {'product': product})