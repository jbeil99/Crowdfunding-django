from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import ActivationToken
from .serializers import UserRegistrationSerializer, LoginSerializer

User = get_user_model()

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = ActivationToken.objects.create(user=user)
            activation_link = f"{settings.FRONTEND_URL}/activate/{token.token}"
            
            html_message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
                'expiry_hours': 24
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                'Activate Your Account',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            return Response({
                "message": "User registered successfully. Please check your email to activate your account."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            activation = ActivationToken.objects.get(token=token)
            if activation.is_valid():
                user = activation.user
                user.is_active = True
                user.save()
                activation.delete()
                return Response({
                    "message": "Account activated successfully. You can now login."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Activation link has expired. Please request a new one."
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ActivationToken.DoesNotExist:
            return Response({
                "message": "Invalid activation link."
            }, status=status.HTTP_400_BAD_REQUEST)



class ResendActivationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({
                    "message": "Account is already activated."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            ActivationToken.objects.filter(user=user).delete()
            
            token = ActivationToken.objects.create(user=user)
            
            activation_link = f"{settings.FRONTEND_URL}/activate/{token.token}"
            
            html_message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
                'expiry_hours': 24
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                'Activate Your Account',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            return Response({
                "message": "Activation email has been sent. Please check your email."
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                "message": "If your email exists in our system, you will receive an activation link."
            }, status=status.HTTP_200_OK)

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer