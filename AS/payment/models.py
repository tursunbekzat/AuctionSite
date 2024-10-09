from django.db import models
from core.models import User, Product

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # pending, completed, failed

    def __str__(self):
        return f'Payment of {self.amount} by {self.user.username} for {self.product.name}'
