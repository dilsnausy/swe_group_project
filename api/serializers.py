from rest_framework import serializers 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # Added import
from users.serializers import UserSerializer  # Added import

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): 
    def validate(self, attrs): 
        data = super().validate(attrs) 
        data['user'] = UserSerializer(self.user).data 
        return data
