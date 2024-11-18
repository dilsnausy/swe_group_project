from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import CustomUser, FarmerProfile, Product
from .serializers import UserSerializer, FarmerProfileSerializer, ProductSerializer
from .forms import BuyerProfileForm


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

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

class ApproveFarmerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        farmer_id = request.data.get('id')
        farmer = FarmerProfile.objects.get(id=farmer_id)
        farmer.is_approved = True
        farmer.save()
        # Send notification to farmer (optional)
        return Response({'status': 'Farmer approved'})

class RejectFarmerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        farmer_id = request.data.get('id')
        feedback = request.data.get('feedback')
        farmer = FarmerProfile.objects.get(id=farmer_id)
        # Send feedback to farmer (e.g., via email)
        farmer.user.delete()  # Remove the user account
        return Response({'status': 'Farmer rejected and account deleted'})

class UsersListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UpdateUserStatusView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get('id')
        status = request.data.get('status')
        user = CustomUser.objects.get(id=user_id)
        user.is_disabled = True if status == 'Disabled' else False
        user.save()
        return Response({'status': f'User status updated to {status}'})

class ProductsListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CreateBuyerProfileView(APIView):
    def get(self, request):
        # This is for rendering an empty form to create a Buyer Profile
        form = BuyerProfileForm()
        return render(request, 'buyer_profile_form.html', {'form': form})

    def post(self, request):
        # This is for handling form submission and saving the Buyer Profile
        form = BuyerProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return Response({'status': 'Buyer profile created successfully'}, status=201)
        return Response({'errors': form.errors}, status=400)