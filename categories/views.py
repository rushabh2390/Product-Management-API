from rest_framework import permissions, status, viewsets
from .models import Category
from .serializers import CategorySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all users
    and write access to admin users only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff  # Admin only for other methods


class CategoryViewSet(viewsets.ModelViewSet):
    # List only non-deleted categories
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.action == 'list':  # Only apply filtering for list action
            return self.queryset.filter(parent__isnull=True)
        elif self.action == 'retrieve':  # For detail view, we want to see all the subcategories
            return self.queryset
        return self.queryset  # For other actions(create, update, del

    @swagger_auto_schema(
        operation_summary="Create a new category",
        tags=["Categories"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=CategorySerializer,
        responses={
            201: openapi.Response(description="Category created", schema=CategorySerializer),
            400: openapi.Response(description="Bad Request"),
            # Adjust permission message
            403: openapi.Response(description="Forbidden (Admin Only)"),
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List top-level categories",
        tags=["Categories"],
        responses={
            200: openapi.Response(description="List of categories", schema=CategorySerializer(many=True)),
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific category",
        tags=["Categories"],
        responses={
            200: openapi.Response(description="Category details", schema=CategorySerializer),
            404: openapi.Response(description="Not Found"),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a category",
        tags=["Categories"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=CategorySerializer,
        responses={
            200: openapi.Response(description="Category updated", schema=CategorySerializer),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a category",
        tags=["Categories"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=CategorySerializer(partial=True),  # Allow partial updates
        responses={
            200: openapi.Response(description="Category updated", schema=CategorySerializer),
            400: openapi.Response(description="Bad Request"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Soft delete a category",
        tags=["Categories"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Bearer Token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            204: openapi.Response(description="Category deleted"),
            403: openapi.Response(description="Forbidden (Admin Only)"),
            404: openapi.Response(description="Not Found"),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
