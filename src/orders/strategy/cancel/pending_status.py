from django.db import OperationalError
from rest_framework import status
from rest_framework.response import Response

from backend.core.enums import OrderStatus

from orders.serializer import OrderSerializer
from . import CancelOrderStrategy

class CancelOrderPendingStrategy(CancelOrderStrategy):
    serializer_class = OrderSerializer

    def get_response(self, order):
        data = {'status': OrderStatus.CANCELED.value}
        serializer = self.serializer_class(order, data=data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OperationalError:
            return Response(
                {'detail':'Database connection error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )