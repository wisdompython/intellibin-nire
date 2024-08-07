from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
#from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.views import ( PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView)
from dj_rest_auth.urls import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView


# serilaizer
from .serializers import *

from .utils import *

class UserRegisterAPIView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            send_otp = send_mail_to_user(serializer.data['email'])
            
            response = {
                'success': True,
                'user': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)
    
class UserLoginAPIView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Does not exist!"
                }
            }
            if CustomUser.objects.filter(username=request.data['email']).exists():
                user = CustomUser.objects.get(username=request.data['email'])
                
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def resend_otp_token(request, *args, **kwargs):
    queryset = CustomUser.objects.all()
    serializers = ResendOTPSerializer(data=request.data)

    if serializers.is_valid():
        get_user = get_object_or_404(CustomUser, email=serializers.data['email']) # true or false
        try:
            mail = send_mail(
                subject="OTP Verification for wastebin",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[get_user.email],
                message=generate_otp()
            )

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            return Response({"failed":f"with error {e}"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.errors)


@api_view(["POST"])
def confirm_otp(request):

    serializer = ConfirmOTPSerializer(data = request.data)

    if serializer.is_valid():

        confirm_otp_code = totp.verify(serializer.data['otp'])

        if confirm_otp_code:
            verified_user = CustomUser.objects.get(email=serializer.data['email'])
            verified_user.verified = True
            verified_user.save()

    
            return Response("You are now verified")
        else:
            return Response(
                "Otp expired or incorrect"
            )
    return Response(serializer.errors)

class UserProfileAPIView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    def get(self, request):
    
        user = CustomUser.objects.get(email=request.user.email)

        return Response(
            {
            'email':user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number
            }
        )
    
    def put(self,request):
        get_user = CustomUser.objects.get(id=request.user.id)
        serializers = UpdateUserProfileSerializer(get_user, data= request.data, partial=True)

        if serializers.is_valid():
   
            serializers.save()

            return Response(
                serializers.data
            )
        return Response(
            serializers.errors
        ) 
    
# class UserPasswordResetAPIView(APIView):

class PasswordChangeAPIView(PasswordChangeView):
    """
    View for changing password.
    Inherits from dj_rest_auth's PasswordChangeView.
    """

class PasswordResetAPIView(PasswordResetView):
    """
    View for initiating password reset process.
    Inherits from dj_rest_auth's PasswordResetView.
    """

class PasswordResetConfirmAPIView(PasswordResetConfirmView):
    """
    View for confirming password reset process.
    Inherits from dj_rest_auth's PasswordResetConfirmView.
    """
    
class LogoutAPIView(LogoutView):
    """
    View for user logout.
    Inherits from dj_rest_auth's LogoutView.
    """