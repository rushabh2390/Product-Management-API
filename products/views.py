from rest_framework import viewsets, permissions, status
from .models import Product, Category  # Import your models
from rest_framework.response import Response
from .serializers import ProductSerializer  # Import your serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission class to allow read access to all, but only admin can create, update, delete
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff


class ProductViewSet(viewsets.ModelViewSet):
    # List only non-deleted products
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.action == 'retrieve': 
            return self.queryset
        return self.queryset

    @swagger_auto_schema(
        operation_summary="Create a new product (Admin Only)",
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(description="Product created", schema=ProductSerializer),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List all products (Public)",
        tags=["Products"],
        responses={
            200: openapi.Response(
                description="List of products", schema=ProductSerializer(many=True)
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific product",
        tags=["Products"],
        responses={
            200: openapi.Response(description="Product details", schema=ProductSerializer),
            404: openapi.Response(description="Not Found"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update product details (Admin Only)",
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=ProductSerializer,
        responses={
            200: openapi.Response(description="Product updated", schema=ProductSerializer),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a product",
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=ProductSerializer(partial=True),  # Allow partial updates
        responses={
            200: openapi.Response(description="product updated", schema=ProductSerializer),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Soft delete a product (Admin Only)",
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            204: openapi.Response(description="Product deleted"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()  # Soft delete
        return Response(status=status.HTTP_204_NO_CONTENT)
