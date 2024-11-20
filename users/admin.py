from django.contrib import admin
from .forms import FarmerProfileForm
from .models import CustomUser, FarmerProfile, BuyerProfile

print("Attempting to register FarmerProfile in users/admin.py")

@admin.register(CustomUser) 
class CustomUserAdmin(admin.ModelAdmin): 
    list_display = ('email', 'phone_number', 'is_active', 'is_staff') 
    search_fields = ('email', 'username', 'phone_number') 
    list_filter = ('is_active', 'is_staff', 'role') 
    ordering = ('email',)

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    form = FarmerProfileForm  # Attach the custom form
    list_display = ('user', 'farm_size', 'location', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'user__email', 'location', 'farm_size')

    actions = ['approve_farmer', 'reject_farmer']

    def approve_farmer(self, request, queryset):
        queryset.update(is_approved=True, rejection_reason=None)
        self.message_user(request, "Selected farmers have been approved.")

    def reject_farmer(self, request, queryset):
        for farmer in queryset:
            farmer.is_approved = False
            farmer.rejection_reason = "Rejected due to incomplete data."
            farmer.save()
        self.message_user(request, "Selected farmers have been rejected.")

    approve_farmer.short_description = "Approve selected farmers"
    reject_farmer.short_description = "Reject selected farmers"

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_address')
    search_fields = ('user__username', 'delivery_address')
