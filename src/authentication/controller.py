from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializer import LoginSerializer
from users.serializer import UserSerializer

from .interfaces.services.auth_service import AuthService


class AuthenticationController:

    def __init__(self, authentication_service:AuthService):
        self.auth_service = authentication_service

    def login(self, request:Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user_serializer = UserSerializer(user)

        session = self.auth_service.create_session(user)
        return Response(
            {
                'user': user_serializer.data, 
                **self.auth_service.session_to_dict(session)
            },
            status=status.HTTP_201_CREATED
        )

