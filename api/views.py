from django.shortcuts import render 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.permissions import IsAdminUser 
from .serializers import CustomTokenObtainPairSerializer  # Added import
from users.permissions import IsFarmer, IsBuyer


class CustomTokenObtainPairView(TokenObtainPairView): 
    serializer_class = CustomTokenObtainPairSerializer

class FarmerView(APIView):
    permission_classes = [IsFarmer]

    def get(self, request):
        # Logic for farmer-only access
        return Response({"message": "Welcome, Farmer!"})

class BuyerView(APIView):
    permission_classes = [IsBuyer]

    def get(self, request):
        # Logic for buyer-only access
        return Response({"message": "Welcome, Buyer!"})


