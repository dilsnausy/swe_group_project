from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from products.models import Product
from users.models import BuyerProfile

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        buyer = BuyerProfile.objects.get(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        if product.quantity < int(quantity):
            return Response({"error": "Insufficient stock."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = product.price * int(quantity)
        order = Order.objects.create(
            buyer=buyer,
            product=product,
            quantity=quantity,
            total_price=total_price,
        )
        product.quantity -= int(quantity)
        product.save()
        return Response({"message": "Order placed successfully!", "order_id": order.id}, status=status.HTTP_201_CREATED)


class BuyerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = BuyerProfile.objects.get(user=request.user)
        orders = Order.objects.filter(buyer=buyer).order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
