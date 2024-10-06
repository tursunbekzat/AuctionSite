from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from authenticate.models import User
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    author = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.current_price is None:  # Устанавливаем начальную цену как текущую при создании
            self.current_price = self.starting_price
        if not self.end_time:  # Устанавливаем время окончания аукциона на 3 дня после создания
            self.end_time = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)

    def is_active(self):
        return timezone.now() < self.end_time

    def extend_auction(self, additional_days):
        self.end_time += timedelta(days=additional_days)
        self.save()
    
    
class Bid(models.Model):
    product = models.ForeignKey(Product, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Проверка, что пользователь не может делать ставку на свой продукт
        if self.product.author == self.user:
            raise ValidationError("Вы не можете делать ставку на свой продукт.")
        else:
            # Проверяем, что ставка больше текущей цены продукта
            if self.amount <= self.product.current_price:
                raise ValueError("Ставка должна быть выше текущей цены.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bid by {self.user.username} for {self.product.name} - ${self.amount}"
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара на момент заказа

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
