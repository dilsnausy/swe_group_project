from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (FarmerViewSet, BuyerViewSet, CustomUserViewSet, LoginAPIView, ProtectedView, FarmerDashboardView, AdminDashboardView,
                    BuyerDashboardView, RegisterView, ProfileView, CreateBuyerProfileView,
                    DashboardStatsView, PendingFarmersView, ApproveFarmerView, RejectFarmerView,
                    UpdateUserStatusView, UsersListView, CreateFarmerProfileView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet, basename='farmers')
router.register(r'buyers', BuyerViewSet, basename='buyers')
router.register(r'customusers', CustomUserViewSet, basename='customusers')

urlpatterns = [
    # Authentication Endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('create_buyer_profile/', views.CreateBuyerProfileView.as_view(), name='create_buyer_profile'),

    # Admin Endpoints
    path('admin/dashboard-stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
    path('admin/pending-farmers/', views.PendingFarmersView.as_view(), name='pending_farmers'),
    path('admin/approve-farmer/', views.ApproveFarmerView.as_view(), name='approve_farmer'),
    path('admin/reject-farmer/', views.RejectFarmerView.as_view(), name='reject_farmer'),
    path('admin/users/', views.UsersListView.as_view(), name='users_list'),
    path('admin/update-user-status/', views.UpdateUserStatusView.as_view(), name='update_user_status'),

    path('', include(router.urls)),
    path('api/user/login', LoginAPIView.as_view(), name='user-login'),
    path('api/protected', ProtectedView.as_view(), name='protected'),
    path('api/farmer-dashboard', FarmerDashboardView.as_view(), name='farmer_dashboard'),
    path('api/admin-dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('api/buyer-dashboard', BuyerDashboardView.as_view(), name='buyer_dashboard'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_farmer_profile/', CreateFarmerProfileView.as_view(), name='create_farmer_profile'),
]   
