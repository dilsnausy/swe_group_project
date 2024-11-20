from django.urls import path
from .views import PlaceOrderView, BuyerOrdersView

urlpatterns = [
    path('place/', PlaceOrderView.as_view(), name='place_order'),
    path('my-orders/', BuyerOrdersView.as_view(), name='buyer_orders'),
]
