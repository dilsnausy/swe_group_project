from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_disabled = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
    )
    email = models.EmailField(max_length=255, unique=True)
    def __str__(self):
        return self.username


class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="buyer_profile")
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Buyer Profile of {self.user.username}"

class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="farmer_profile")
    farm_size = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Farmer Profile of {self.user.username}"

    def str(self):
        return f"{self.user.username}'s Profile"

class Product(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField()
    # Add image fields as necessary

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="images")
    image_url = models.TextField()

    def __str__(self):
        return f"Image for product {self.product.name}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."
