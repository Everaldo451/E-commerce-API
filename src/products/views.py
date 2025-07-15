from django.db import OperationalError

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from backend.core.permissions import IsOwnerOrReadOnly

from .models import Product
from .serializer import ProductSerializer, SearchSerializer

class ProductViewsets(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('tags', 'media').select_related('created_by')
    serializer_class = ProductSerializer
    permission_classes=(permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @swagger_auto_schema(
        operation_description = 'Login the user in the API',
        query_serializer=SearchSerializer,
        responses={
            200: ProductSerializer(many=True),
        }
    )
    @action(detail=False, methods=["GET"])
    def search(self, request:Request):
        serializer = SearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        filters = serializer.validated_data.copy()
        keys_to_update = []

        for key in filters:
            if isinstance(serializer.fields[key], serializers.ManyRelatedField):
                keys_to_update.append(key)

        for key in keys_to_update:
            filters[f'{key}__in'] = filters.pop(key)

        try:
            products = Product.objects.filter(**filters).all()
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OperationalError:
            return Response(
                {"detail": "Database connection error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

