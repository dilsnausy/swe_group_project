from django.contrib import admin
from .models import Notification
from .forms import NotificationForm

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm  # Use the custom form
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        # Ensure no empty messages are marked as read
        queryset.filter(message__isnull=False).update(is_read=True)
        self.message_user(request, "Selected notifications marked as read.")

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Selected notifications marked as unread.")

    mark_as_read.short_description = "Mark selected notifications as read"
    mark_as_unread.short_description = "Mark selected notifications as unread"
