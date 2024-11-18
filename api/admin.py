from django.contrib import admin
from .models import BuyerProfile, Notification, ProductImage, FarmerProfile

admin.site.register(BuyerProfile)
admin.site.register(Notification)
admin.site.register(ProductImage)
admin.site.register(FarmerProfile)