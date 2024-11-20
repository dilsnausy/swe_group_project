from django.urls import path
from .views import ProductListView, AddProductView, ProductViewSet

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('add/', AddProductView.as_view(), name='add-product'),
    path('', ProductViewSet.as_view({'get': 'list'}), name='product-root'),
]
