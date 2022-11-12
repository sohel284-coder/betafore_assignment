from django.urls import path

from accountapp.views import *


urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),

    path('otp-login/', LoginWithOtp.as_view(), name='otp_login'),
    path('verify/', OtpVerificationForLogin.as_view(), name='verify'),

]