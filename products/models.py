from django.db import models
from users.models import FarmerProfile

class Product(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    
    # Add image fields as necessary


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"  # Ensure this related_name exists
    )
    image_url = models.TextField()

    def __str__(self):
        return f"Image for product {self.product.name}"