from django.urls import path
from .views import (
    CustomTokenObtainPairView, DashboardStatsView, PendingFarmersView,
    ApproveFarmerView, RejectFarmerView, UsersListView,
    UpdateUserStatusView, ProductsListView, CreateBuyerProfileView
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/dashboard-stats/', DashboardStatsView.as_view()),
    path('admin/pending-farmers/', PendingFarmersView.as_view()),
    path('admin/approve-farmer/', ApproveFarmerView.as_view()),
    path('admin/reject-farmer/', RejectFarmerView.as_view()),
    path('admin/users/', UsersListView.as_view()),
    path('admin/update-user-status/', UpdateUserStatusView.as_view()),
    path('admin/products/', ProductsListView.as_view()),
    path('create_buyer_profile/', CreateBuyerProfileView.as_view(), name='create_buyer_profile'),
]
