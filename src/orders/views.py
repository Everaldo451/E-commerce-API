from rest_framework import viewsets, permissions

from backend.core.permissions import IsOwner, IsAdminOrOwner

from .models import Order
from .serializer import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('products','created_by')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return (permissions.IsAuthenticated(),)
        return (permissions.IsAuthenticated(), IsAdminOrOwner())
