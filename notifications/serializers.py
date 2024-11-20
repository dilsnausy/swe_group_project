from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer  # Ensure this serializer exists

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested serializer for user details

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'user', 'created_at']