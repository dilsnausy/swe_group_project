from rest_framework import serializers 
from .models import Product, ProductImage 
from users.serializers import FarmerProfileSerializer  # Added import
from users.models import FarmerProfile

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

class ProductSerializer(serializers.ModelSerializer):
    # Allow input for farmer as a PrimaryKeyRelatedField
    farmer = serializers.PrimaryKeyRelatedField(queryset=FarmerProfile.objects.all())
    images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for images

    class Meta:
        model = Product
        fields = '__all__'

    def validate_farmer(self, value):
        if not value.is_approved:
            raise serializers.ValidationError("The farmer is not approved to create products.")
        return value
