from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/products/', include('products.urls')),  # API for products
    # path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('notifications/', include('notifications.urls')),

    path('api/users/', include('users.urls')),  # Add this line

    path('', include('users.urls')),
    path('api/', include('users.urls')),  # Include app-level URLs

    path('orders/', include('orders.urls')),
]