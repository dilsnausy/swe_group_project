from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'total_price', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('buyer__user__email', 'product__name')
