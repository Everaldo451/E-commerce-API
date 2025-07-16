from rest_framework import status
from rest_framework.response import Response
from . import CancelOrderStrategy

class CancelOrderOtherStatusStrategy(CancelOrderStrategy):

    def get_response(self, order):
        return Response(
            {'detail': "Forbidden. The current status doesn't allow cancellation."},
            status=status.HTTP_403_FORBIDDEN
        )