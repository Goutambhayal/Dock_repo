from django.urls import path
from .views import RegisterView, LoginView,  VerifyOTPView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('users/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp')
] 