from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from backend.core.permissions import IsAdminOrOwner

from .models import Order
from .serializer import OrderSerializer
from .strategy.cancel.get_strategy import get_strategy_based_in_order_status

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('products','created_by')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return (permissions.IsAuthenticated(),)
        return (permissions.IsAuthenticated(), IsAdminOrOwner())

    @swagger_auto_schema(
        operation_description = 'Cancel the order if is pending.',
        request_body=None,
        responses={
            200: OrderSerializer,
        }
    )
    @action(
        detail=True, 
        methods=['patch'],
        serializer_class = None,
        permission_classes=[permissions.IsAuthenticated, IsAdminOrOwner]
    )
    def cancel(self, request, pk=None):
        order = self.get_object()

        strategy = get_strategy_based_in_order_status(request, order.status)
        return strategy.get_response(order)
