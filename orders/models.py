from django.db import models
from users.models import BuyerProfile
from products.models import Product

class Order(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"Order {self.id} by {self.buyer.user.email}"
