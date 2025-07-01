from rest_framework import viewsets, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import Product
from .serializer import ProductSerializer, SearchSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=False, methods=["GET"])
    def search(self, request:Request):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products = Product.objects.filter(**serializer.validated_data).all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
