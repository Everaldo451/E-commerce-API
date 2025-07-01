from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from drf_yasg.utils import swagger_auto_schema

from .services.jwt_auth_service import JWTAuthService
from .controller import AuthenticationController
from .serializer import LoginSerializer, LoginResponseSerializer, LogoutResponseSerializer, RefreshResponseSerializer

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


class RefreshView(TokenRefreshView):

    @swagger_auto_schema(
        responses={
            200: RefreshResponseSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code==status.HTTP_200_OK:
            response = Response({
                    "access_token": response.data['access']
                }, 
                status=status.HTTP_200_OK
            )
        return response
    

class LogoutView(TokenBlacklistView):
    
    @swagger_auto_schema(
        operation_description='Logout the user in the API',
        responses={
            200: LogoutResponseSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)




# Create your views here.
