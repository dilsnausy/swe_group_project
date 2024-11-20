from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from users.permissions import IsFarmer
from rest_framework.response import Response


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFarmer]  # Only farmers can access

    def get_queryset(self):
        # Restrict products to those owned by the authenticated farmer
        if self.request.user.is_farmer():
            return Product.objects.filter(farmer=self.request.user.farmer_profile)
        return Product.objects.none()  # Return no products for non-farmers

class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()  # List all products

    def get_queryset(self):
        # Optionally filter by category, price range, etc.
        category = self.request.query_params.get("category")
        if category:
            return Product.objects.filter(category=category)
        return super().get_queryset()

class AddProductView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]  # Restrict to authenticated farmers

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(farmer=request.user.farmer_profile)  # Ensure the farmer is linked
            return Response({
                "message": "Product added successfully!",
                "product": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)