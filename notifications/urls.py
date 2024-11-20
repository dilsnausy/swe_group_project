from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/', views.MarkNotificationsReadView.as_view(), name='mark-notifications-read'),
]
