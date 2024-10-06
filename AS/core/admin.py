from django.contrib import admin
from .models import User, Category, Product, Bid, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_price', 'author', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'created_at')  # Поля для отображения
    list_filter = ('product',)  # Фильтрация по продукту


admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
