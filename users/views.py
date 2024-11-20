from django.shortcuts import render 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated 
from users.permissions import IsFarmer, IsBuyer
from .models import CustomUser, FarmerProfile, BuyerProfile
from .serializers import BuyerProfileSerializer, UserSerializer, FarmerProfileSerializer, RegisterSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
import logging
from .permissions import IsAdmin

logger = logging.getLogger(__name__)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You have accessed a protected endpoint!"})


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        logger.debug(f"Login attempt: {email}")

        user = authenticate(username=email, password=password)
        if user:
            logger.debug(f"Authenticated user: {user.email}")
            # Check if user is inactive or disabled
            if not user.is_active:
                return Response({"error": "User is inactive."}, status=status.HTTP_403_FORBIDDEN)
            if user.is_disabled:
                return Response({"error": "Your account is disabled."}, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role,
            }, status=status.HTTP_200_OK)

        logger.debug("Authentication failed.")
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info(f"Incoming registration data: {request.data}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            logger.info(f"New user registered: {user.email}")
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Restrict to authenticated admins

    def get(self, request):
        total_users = CustomUser.objects.count()
        total_farmers = FarmerProfile.objects.count()
        total_buyers = BuyerProfile.objects.count()
        pending_farmers = FarmerProfile.objects.filter(is_approved=False).count()

        return Response({
            "message": "Welcome to the Admin Dashboard!",
            "statistics": {
                "total_users": total_users,
                "total_farmers": total_farmers,
                "total_buyers": total_buyers,
                "pending_farmer_approvals": pending_farmers,
            },
        })

class BuyerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]  # Restrict to authenticated buyers

    def get(self, request):
        buyer_profile = request.user.buyer_profile  # Assuming the related_name="buyer_profile" is set
        return Response({
            "message": "Welcome to the Buyer Dashboard!",
            "buyer_details": {
                "email": request.user.email,
                "delivery_address": buyer_profile.delivery_address,
            },
            # Add order history if available
            # "order_history": [{"order_id": 1, "items": ["item1", "item2"]}, ...],
        })

class FarmerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsFarmer]  # Restrict to authenticated farmers

    def get(self, request):
        farmer_profile = request.user.farmer_profile  # Assuming the related_name="farmer_profile" is set
        return Response({
            "message": "Welcome to the Farmer Dashboard!",
            "farmer_details": {
                "email": request.user.email,
                "farm_size": farmer_profile.farm_size,
                "location": farmer_profile.location,
                "is_approved": farmer_profile.is_approved,
                "rejection_reason": farmer_profile.rejection_reason if not farmer_profile.is_approved else None,
            },
        })

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

class CustomUserViewSet(ModelViewSet):
    """
    A viewset for viewing and editing CustomUser instances.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class FarmerViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing farmers.
    """
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer
    permission_classes = [IsAuthenticated]

class BuyerViewSet(ModelViewSet):
    queryset = BuyerProfile.objects.all()
    serializer_class = BuyerProfileSerializer
    permission_classes = [IsAuthenticated]

class DashboardStatsView(APIView): 
    permission_classes = [IsAdminUser] 

    def get(self, request): 
        total_users = CustomUser.objects.count() 
        pending_farmers = FarmerProfile.objects.filter(is_approved=False).count() 
        disabled_accounts = CustomUser.objects.filter(is_disabled=True).count() 
        return Response({ 
            'totalUsers': total_users, 
            'pendingFarmers': pending_farmers, 
            'disabledAccounts': disabled_accounts, 
        }) 

class PendingFarmersView(APIView): 
    permission_classes = [IsAdminUser] 

    def get(self, request): 
        pending_farmers = FarmerProfile.objects.filter(is_approved=False) 
        serializer = FarmerProfileSerializer(pending_farmers, many=True) 
        return Response(serializer.data) 

from django.shortcuts import get_object_or_404

class ApproveFarmerView(APIView): 
    permission_classes = [IsAdminUser] 

    def post(self, request): 
        farmer_id = request.data.get('id') 
        farmer = get_object_or_404(FarmerProfile, id=farmer_id)
        farmer.is_approved = True 
        farmer.save() 
        # Send notification to farmer (optional) 
        return Response({'status': 'Farmer approved'}) 

class RejectFarmerView(APIView): 
    permission_classes = [IsAdminUser] 

    def post(self, request): 
        farmer_id = request.data.get('id') 
        feedback = request.data.get('feedback') 
        farmer = get_object_or_404(FarmerProfile, id=farmer_id)
        # Send feedback to farmer (e.g., via email) 
        farmer.user.delete()  # Remove the user account 
        return Response({'status': 'Farmer rejected and account deleted'}) 

class UpdateUserStatusView(APIView): 
    permission_classes = [IsAdminUser] 

    def post(self, request): 
        user_id = request.data.get('id') 
        status = request.data.get('status') 
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_disabled = True if status == 'Disabled' else False 
        user.save() 
        return Response({'status': f'User status updated to {status}'})

class CreateBuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request):
        # Automatically link the authenticated user
        data = request.data.copy()
        data['user'] = request.user.id  # Set user field based on the authenticated user
        serializer = BuyerProfileSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            buyer_profile = serializer.save()
            return Response({
                'status': 'Buyer profile created successfully',
                'buyer_profile': BuyerProfileSerializer(buyer_profile).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CreateFarmerProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request, *args, **kwargs):
        # Automatically link the authenticated user
        user = request.user
        if FarmerProfile.objects.filter(user=user).exists():
            return Response(
                {"error": "Farmer profile already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FarmerProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            farmer_profile = serializer.save()
            return Response(
                {
                    "status": "Farmer profile created successfully",
                    "farmer_profile": FarmerProfileSerializer(farmer_profile).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UsersListView(APIView): 
    permission_classes = [IsAdminUser] 

    def get(self, request): 
        users = CustomUser.objects.all() 
        serializer = UserSerializer(users, many=True) 
        return Response(serializer.data) 
