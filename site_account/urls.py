from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('login/auth/', views.AuthView),
    path('login/auth/password/', views.AuthPasswordView),
    path('login/auth/otp/', views.AuthOTPView),
    path('login/auth/resendotp/', views.ResendOTPView),
    path('login/auth/sendtootpsection/', views.SendToOTPSection),
    path('login/auth/sendtoresetpasswordsection/', views.SendToResetPasswordSection),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),

]
