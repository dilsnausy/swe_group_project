from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListCreateAPIView):
    """
    API view to retrieve the list of notifications for the current user or create a new notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a notification instance.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = request.data.get('is_read', instance.is_read)
        instance.save()
        return Response(NotificationSerializer(instance).data, status=status.HTTP_200_OK)

class MarkNotificationsReadView(APIView):
    """
    API view to mark multiple notifications as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Mark all notifications as read for the authenticated user
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({"status": "All notifications marked as read."})