from django.urls import path, include
from .views import RegistrationView, LoginView, LogoutView, UserUpdateView, ForgotPasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('update/', UserUpdateView.as_view(), name="user-update"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
]
