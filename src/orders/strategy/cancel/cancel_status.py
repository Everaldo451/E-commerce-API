from rest_framework import status
from rest_framework.response import Response
from . import CancelOrderStrategy

class CancelOrderCanceledStrategy(CancelOrderStrategy):

    def get_response(self, order):
        return Response(
            {'detail': "Order is already canceled."},
            status=status.HTTP_400_BAD_REQUEST
        )