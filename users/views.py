# from acuity_api.settings import GET_STREAM_API_KEY, GET_STREAM_SECRET_KEY
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from .models import CustomerUser
from .serializers import RegistrationSerializer, UserUpdateSerializer, LoginSerializer, DetailSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, Schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.http import Http404
import logging
import traceback
logger = logging.getLogger('PM')


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        tags=["Users"],
        operation_id="create_user",
        operation_description="Create Product management users",
        operation_summary="Create Product management users",
        request_body=RegistrationSerializer,
        responses={201: openapi.Response(
            description='Create product management users', schema=DetailSerializer), 500: 'Internal server error'}
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(DetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        tags=["Users"],
        operation_id="login_user",
        operation_description="Login User",
        operation_summary="Login User",
        request_body=LoginSerializer,  # Use the serializer directly
        responses={
            200: openapi.Response(
                description='User login successful',
                schema=openapi.Schema(  # Define the 200 response schema
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, description="Access token"),
                    },
                    required=["refresh", "access"],  # Both tokens are returned
                ),
            ),
            # More specific message
            400: openapi.Response(description='Bad Request. Invalid input data.'),
            # 401 for authentication errors
            401: openapi.Response(description='Unauthorized. Invalid credentials.'),
            # Use openapi.Response
            500: openapi.Response(description='Internal Server Error'),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomerUser.objects.get(email=email)
            except CustomerUser.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (JWTAuthentication,)

    @swagger_auto_schema(
        tags=["Users"],
        operation_id="Logout_user",
        operation_description="Logout User",
        operation_summary="Logout User",
        request_body=openapi.Schema(  # Define request body for refresh token
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
            },
            required=["refresh"],  # refresh token is required
        ),
        responses={
            # Correct description
            205: openapi.Response(description='User logout successful'),
            # More specific error message
            400: openapi.Response(description='Bad Request. Refresh token is required or invalid.'),
            # Use openapi.Response
            500: openapi.Response(description='Internal Server Error'),
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserUpdateView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        tags=["Users"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        operation_id="Update_user",
        operation_description="Update User",
        operation_summary="Update User",
        request_body=UserUpdateSerializer,
        responses={200: openapi.Response(
            description='User detail update', schema=DetailSerializer), 500: 'Internal server error'}
    )
    def patch(self, request):
        user = request.user
        # partial=True for partial updates
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(DetailSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        tags=["Users"],
        request_body=openapi.Schema(  # Define the request body schema
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email address"),
            },
            required=['email'],  # Email is a required field
        ),
        responses={
            200: openapi.Response(description='Password reset email sent'),
            404: openapi.Response(description='User with this email does not exist'),
            500: openapi.Response(description='Failed to send email'),
        },
        operation_summary="Send password reset link",
        # Add a description
        operation_description="Sends a password reset link to the user's email address.",
    )
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomerUser.objects.get(email=email)
            # Generate a password reset token (you'll need to implement this)
            # For simplicity, I am generating a random password and setting it for the user.
            import random
            import string
            new_password = ''.join(random.choice(
                string.ascii_letters + string.digits) for i in range(10))
            user.set_password(new_password)
            user.save()
            # Send email with the reset link (replace with your actual email sending logic)
            send_mail(
                'Password Reset',
                # In real app, send reset link
                f'Your new password is: {new_password}',
                settings.EMAIL_HOST_USER,  # From email
                [email],  # To email
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)

        except CustomerUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
