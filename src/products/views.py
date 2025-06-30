from rest_framework import viewsets, permissions
from .models import Product
from .serializer import ProductSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
