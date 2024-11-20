from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from api.views import CustomTokenObtainPairView
from users.views import (
    DashboardStatsView, PendingFarmersView,
    ApproveFarmerView, RejectFarmerView, UsersListView,
    UpdateUserStatusView
)
from rest_framework_simplejwt.views import TokenVerifyView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/dashboard-stats/', DashboardStatsView.as_view()),
    path('admin/pending-farmers/', PendingFarmersView.as_view()),
    path('admin/approve-farmer/', ApproveFarmerView.as_view()),
    path('admin/reject-farmer/', RejectFarmerView.as_view()),
    path('admin/users/', UsersListView.as_view()),
    path('admin/update-user-status/', UpdateUserStatusView.as_view()),
    path('', include(router.urls)),  # Includes all router-based endpoints
]
