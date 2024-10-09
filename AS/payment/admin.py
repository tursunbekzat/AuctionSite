from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'status', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
