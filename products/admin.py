from django.utils.html import format_html
from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):  # Inline for product images
    model = ProductImage
    extra = 1

    # Display the image preview in the inline
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_url:  # Check if the image_url is not empty
            return format_html(f'<img src="{obj.image_url}" style="max-height: 100px;"/>')
        return "No image available"

    image_preview.short_description = "Image Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'farmer')
    list_filter = ('category', 'farmer')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]  # Include inline for images
