from rest_framework import serializers
from .models import CustomUser, FarmerProfile, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'is_disabled')

class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FarmerProfile
        fields = ('id', 'user', 'farm_size', 'location', 'is_approved')

class ProductSerializer(serializers.ModelSerializer):
    farmer = FarmerProfileSerializer()

    class Meta:
        model = Product
        fields = '__all__'
