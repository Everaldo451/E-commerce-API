from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializer import UserSerializer

from .services.jwt_auth_service import JWTAuthService
from .controller import AuthenticationController
from .serializer import LoginSerializer, LoginResponseSerializer

auth_controller = AuthenticationController(JWTAuthService())

class LoginView(APIView):

    @swagger_auto_schema(
        operation_description = 'Login the user in the API',
        request_body=LoginSerializer,
        responses={
            201: LoginResponseSerializer,
        }
    )
    def post(self, request, format=None):
        return auth_controller.login(request)


class LogonView(APIView):
    pass




# Create your views here.
