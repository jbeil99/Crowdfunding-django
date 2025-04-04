from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView, 
    ActivateAccountView,
    ResendActivationView,
    LoginView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uuid:token>/', ActivateAccountView.as_view(), name='activate'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-activation/', ResendActivationView.as_view(), name='resend_activation'),
    path('login/', LoginView.as_view(), name='login'),

]
