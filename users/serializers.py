# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BuyerProfile, FarmerProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_disabled', 'phone_number']
        read_only_fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # If the user is a farmer, create a FarmerProfile
        if user.role == 'farmer':
            FarmerProfile.objects.create(user=user, farm_size='', location='')
        # If the user is a buyer, create a BuyerProfile
        elif user.role == 'buyer':
            BuyerProfile.objects.create(user=user, delivery_address='')
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number']

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['user', 'farm_size', 'location', 'is_approved', 'rejection_reason']
        extra_kwargs = {
            'user': {'read_only': True},
            'is_approved': {'read_only': True},
            'rejection_reason': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user  # Get the authenticated user
        return FarmerProfile.objects.create(user=user, **validated_data)

class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['delivery_address']

    def validate(self, data):
        user = self.context['request'].user
        if BuyerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("Buyer profile already exists for this user.")
        return data
        