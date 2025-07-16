from abc import ABC, abstractmethod
from rest_framework.response import Response

class CancelOrderStrategy(ABC):

    def __init__(self, request):
        self.request = request

    @abstractmethod
    def get_response(self, order) -> Response:
        pass