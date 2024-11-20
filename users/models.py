from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models 
from django.core.validators import RegexValidator 

class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model, using email as the unique identifier.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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
    email = models.EmailField(max_length=255, unique=True)  # Use email as the primary identifier

    # Set email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No additional fields are required

    # Assign the custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email  # Return email as the string representation

    # Utility methods for role checks
    def is_admin(self):
        return self.role == 'admin'

    def is_farmer(self):
        return self.role == 'farmer'

    def is_buyer(self):
        return self.role == 'buyer'


class BuyerProfile(models.Model): 
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="buyer_profile") 
    delivery_address = models.CharField(max_length=255) 

    def __str__(self): 
        return f"Buyer Profile of {self.user.email}" 

class FarmerProfile(models.Model): 
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="farmer_profile") 
    farm_size = models.CharField(max_length=100) 
    location = models.CharField(max_length=255) 
    is_approved = models.BooleanField(default=False) 
    rejection_reason = models.TextField(null=True, blank=True) 

    def __str__(self):  # Remove the incorrect `str` method
        return f"Farmer Profile of {self.user.email}"
