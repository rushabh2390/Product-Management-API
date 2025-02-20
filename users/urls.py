from django.urls import path, include
from .views import RegistrationView, LoginView, LogoutView, UserUpdateView, ForgotPasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
]